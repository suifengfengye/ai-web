from langchain.agents import create_agent, AgentState
from langchain_openai import ChatOpenAI
from prompts import system_prompt
from langchain.tools import tool
from wikipedia_tool import search_wikipedia
from weather_tool import get_weather_forecast
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, ToolMessage
import asyncio
import json
import os
import requests

_ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(_ENV_PATH)

def _get_dify_data_api_key() -> str | None:
    api_key = os.getenv("DIFY_DATA_API_KEY")
    if api_key:
        return api_key
    load_dotenv(_ENV_PATH, override=False)
    return os.getenv("DIFY_DATA_API_KEY")

def _get_openai_api_key() -> str | None:
    api_key = os.getenv("OPEN_AI_APIKEY")
    if api_key:
        return api_key
    load_dotenv(_ENV_PATH, override=False)
    return os.getenv("OPEN_AI_APIKEY")

def _find_dataset_id_by_name(*, base_url: str, api_key: str, dataset_name: str) -> str | None:
    headers = {"Authorization": f"Bearer {api_key}"}
    page = 1
    limit = 100
    while True:
        resp = requests.get(
            f"{base_url}/datasets",
            headers=headers,
            params={"page": page, "limit": limit},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        datasets = data.get("data") or []
        for ds in datasets:
            if ds.get("name") == dataset_name and ds.get("id"):
                return ds["id"]
        if not data.get("has_more"):
            return None
        page += 1

@tool
def search_dify_knowledge_base(query: str) -> str:
    """从 Dify 知识库中检索与查询相关的内容片段。"""
    # search_dify_knowledge_base.__doc__ = ""
    api_key = _get_dify_data_api_key()
    if not api_key:
        return "未找到 DIFY_DATA_API_KEY，请检查根目录 .env 文件。"

    base_url = "https://api.dify.ai/v1"
    dataset_name = "guilin.txt..."

    try:
        dataset_id = _find_dataset_id_by_name(
            base_url=base_url,
            api_key=api_key,
            dataset_name=dataset_name,
        )
        if not dataset_id:
            return f"未找到知识库：{dataset_name}"

        resp = requests.post(
            f"{base_url}/datasets/{dataset_id}/retrieve",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"query": query},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json() if resp.content else {}

        records = data.get("records") or []
        if not records:
            return "知识库未检索到相关内容。"

        lines: list[str] = []
        for i, record in enumerate(records[:5], start=1):
            segment = record.get("segment") or {}
            content = (segment.get("content") or "").strip()
            if not content:
                continue
            score = record.get("score")
            doc = (segment.get("document") or {}).get("name")
            header_parts = [f"[{i}]"]
            if doc:
                header_parts.append(str(doc))
            if score is not None:
                header_parts.append(f"score={score}")
            header = " ".join(header_parts)
            lines.append(f"{header}\n{content}")

        return "\n\n".join(lines) if lines else "知识库检索返回为空。"
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        body = ""
        try:
            body = e.response.text if e.response is not None else ""
        except Exception:
            body = ""
        body = (body or "").strip()
        if len(body) > 800:
            body = body[:800] + "..."
        if status:
            return f"Dify 请求失败（HTTP {status}）。{body}"
        return f"Dify 请求失败。{str(e)}"
    except Exception as e:
        return f"知识库检索异常：{str(e)}"

def dxh_agent():
    openai_api_key = _get_openai_api_key()
    if not openai_api_key:
        raise ValueError("未找到 OPEN_AI_APIKEY，请检查根目录 .env 文件。")
    agent = create_agent(
        model=ChatOpenAI(
            model="gpt-5-mini",
            base_url="https://api.openai-hk.com/v1",
            api_key=openai_api_key,
        ),
        tools=[search_dify_knowledge_base, search_wikipedia, get_weather_forecast],
        system_prompt=system_prompt,
    )
    return agent

def _normalize_messages(item):
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]

def _stringify_payload(payload):
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    try:
        return json.dumps(payload, ensure_ascii=False)
    except Exception:
        return str(payload)

def _is_empty_payload(payload):
    if payload is None:
        return True
    if payload == "":
        return True
    if payload == {}:
        return True
    if payload == "null":
        return True
    if isinstance(payload, str) and payload.strip() in {"", "{}"}:
        return True
    return False

def _extract_tool_calls(message):
    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        return tool_calls
    tool_call_chunks = getattr(message, "tool_call_chunks", None) or []
    if tool_call_chunks:
        calls = []
        for chunk in tool_call_chunks:
            call_id = getattr(chunk, "id", None) if not isinstance(chunk, dict) else chunk.get("id")
            name = getattr(chunk, "name", None) if not isinstance(chunk, dict) else chunk.get("name")
            args = getattr(chunk, "args", None) if not isinstance(chunk, dict) else chunk.get("args")
            calls.append({"id": call_id, "name": name, "args": args, "_is_chunk": True})
        return calls
    additional_kwargs = getattr(message, "additional_kwargs", None) or {}
    return additional_kwargs.get("tool_calls") or []

def _get_tool_name_and_args(tool_call):
    name = tool_call.get("name")
    args = tool_call.get("args")
    if name or args:
        return name, args
    function = tool_call.get("function") or {}
    return function.get("name"), function.get("arguments")

def _is_message_event(event):
    return isinstance(event, BaseMessage)

def _unpack_stream_event(event):
    if isinstance(event, dict):
        return "updates", event
    if isinstance(event, tuple) and len(event) == 2:
        mode, payload = event
        if isinstance(mode, str):
            return mode, payload
        if _is_message_event(mode):
            return "messages", event
    if _is_message_event(event):
        return "messages", event
    return "updates", {"event": event}

def _handle_tool_messages(messages, tool_call_map, tool_request_map, printed_tool_calls):
    for message in messages:
        if isinstance(message, ToolMessage):
            tool_call_id = getattr(message, "tool_call_id", None)
            if tool_call_id and tool_call_id in printed_tool_calls:
                continue
            if tool_call_id:
                printed_tool_calls.add(tool_call_id)
            tool_name = getattr(message, "name", None) or tool_call_map.get(tool_call_id)
            if tool_name:
                print(f"调用工具 {tool_name}")
            else:
                print("调用工具 unknown")
            request_payload = tool_request_map.get(tool_call_id, "")
            print(f"请求体：{request_payload}")
            print(f"返回结果：{_stringify_payload(message.content)}")
            print("--------------------------------------")

def _handle_tool_calls(messages, tool_call_map, tool_request_map, printed_tool_calls):
    for message in messages:
        if isinstance(message, (AIMessage, AIMessageChunk)):
            tool_calls = _extract_tool_calls(message)
            for tool_call in tool_calls:
                tool_name, tool_args = _get_tool_name_and_args(tool_call)
                tool_call_id = tool_call.get("id")
                if tool_call_id and tool_name:
                    tool_call_map[tool_call_id] = tool_name
                request_payload = _stringify_payload(tool_args)
                is_chunk = bool(tool_call.get("_is_chunk")) and isinstance(tool_args, str)
                if tool_call_id:
                    if not _is_empty_payload(request_payload):
                        if is_chunk and tool_request_map.get(tool_call_id):
                            tool_request_map[tool_call_id] = tool_request_map[tool_call_id] + request_payload
                        else:
                            tool_request_map[tool_call_id] = request_payload
                else:
                    if not _is_empty_payload(request_payload):
                        if is_chunk and tool_request_map.get(None):
                            tool_request_map[None] = tool_request_map[None] + request_payload
                        else:
                            tool_request_map[None] = request_payload

def _process_message(message, tool_call_map, tool_request_map, printed_tool_calls, answer_started):
    if isinstance(message, ToolMessage):
        _handle_tool_messages([message], tool_call_map, tool_request_map, printed_tool_calls)
        return answer_started
    if isinstance(message, (AIMessage, AIMessageChunk)):
        tool_calls = _extract_tool_calls(message)
        if tool_calls:
            _handle_tool_calls([message], tool_call_map, tool_request_map, printed_tool_calls)
            return answer_started
        content = getattr(message, "content", "")
        if content:
            if not answer_started:
                print("回答正文：", end="", flush=True)
                answer_started = True
            print(content, end="", flush=True)
    return answer_started

def run_stream(agent, user_message):
    inputs = {"messages": [{"role": "user", "content": user_message}]}
    tool_call_map = {}
    tool_request_map = {}
    printed_tool_calls = set()
    answer_started = False
    print("开始调用....")
    try:
        stream = agent.stream(inputs, stream_mode=["updates", "messages"])
    except TypeError:
        stream = agent.stream(inputs, stream_mode="updates")
    for event in stream:
        mode, payload = _unpack_stream_event(event)
        # print(mode, payload)
        if mode == "messages":
            if isinstance(payload, tuple) and len(payload) == 2 and _is_message_event(payload[0]):
                message, _metadata = payload
            elif _is_message_event(payload):
                message = payload
            else:
                message = None
            if message is not None:
                answer_started = _process_message(
                    message,
                    tool_call_map,
                    tool_request_map,
                    printed_tool_calls,
                    answer_started,
                )
            continue
        if isinstance(payload, dict):
            messages = _normalize_messages(payload.get("messages"))
            for message in messages:
                answer_started = _process_message(
                    message,
                    tool_call_map,
                    tool_request_map,
                    printed_tool_calls,
                    answer_started,
                )
    if answer_started:
        print()
    print("调用结束!!!")

async def run_astream(agent, user_message):
    inputs = {"messages": [{"role": "user", "content": user_message}]}
    tool_call_map = {}
    tool_request_map = {}
    printed_tool_calls = set()
    answer_started = False
    print("开始调用....")
    try:
        stream = agent.astream(inputs, stream_mode=["updates", "messages"])
    except TypeError:
        stream = agent.astream(inputs, stream_mode="updates")
    async for event in stream:
        mode, payload = _unpack_stream_event(event)
        if mode == "messages":
            if isinstance(payload, tuple) and len(payload) == 2 and _is_message_event(payload[0]):
                message, _metadata = payload
            elif _is_message_event(payload):
                message = payload
            else:
                message = None
            if message is not None:
                answer_started = _process_message(
                    message,
                    tool_call_map,
                    tool_request_map,
                    printed_tool_calls,
                    answer_started,
                )
            continue
        if isinstance(payload, dict):
            messages = _normalize_messages(payload.get("messages"))
            for message in messages:
                answer_started = _process_message(
                    message,
                    tool_call_map,
                    tool_request_map,
                    printed_tool_calls,
                    answer_started,
                )
    if answer_started:
        print()
    print("调用结束!!!")

if __name__ == "__main__":
    agent = dxh_agent()
    user_message = "请你提供一份广州3天的旅游攻略，出行时间为2026.2.25到2026.2.27"
    # run_stream(agent, user_message)
    asyncio.run(run_astream(agent, user_message))
