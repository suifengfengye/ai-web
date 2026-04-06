from langchain.agents import create_agent, AgentState
from langchain_openai import ChatOpenAI
from prompts import system_prompt
from wikipedia_tool import search_wikipedia
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import atexit
import asyncio
import json
import os
import requests
import subprocess
import sys
import time
from urllib.parse import urlparse

_ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(_ENV_PATH)
_KNOWLEDGE_BASE_MCP_PROCESS: subprocess.Popen | None = None

def _get_openai_api_key() -> str | None:
    api_key = os.getenv("OPEN_AI_APIKEY")
    if api_key:
        return api_key
    load_dotenv(_ENV_PATH, override=False)
    return os.getenv("OPEN_AI_APIKEY")

def _get_openai_base_url() -> str:
    configured = os.getenv("OPEN_AI_BASE_URL")
    if configured and configured.strip():
        return configured.strip()
    return "https://api.openai-hk.com/v1"

def _configure_no_proxy_for_base_url(base_url: str):
    host = urlparse(base_url).hostname
    if not host:
        return
    for key in ("NO_PROXY", "no_proxy"):
        current = os.getenv(key, "")
        entries = [item.strip() for item in current.split(",") if item.strip()]
        if host not in entries:
            entries.append(host)
            os.environ[key] = ",".join(entries)

# def _cleanup_knowledge_base_mcp_server():
#     global _KNOWLEDGE_BASE_MCP_PROCESS
#     if _KNOWLEDGE_BASE_MCP_PROCESS is None:
#         return
#     if _KNOWLEDGE_BASE_MCP_PROCESS.poll() is None:
#         _KNOWLEDGE_BASE_MCP_PROCESS.terminate()
#         try:
#             _KNOWLEDGE_BASE_MCP_PROCESS.wait(timeout=3)
#         except Exception:
#             _KNOWLEDGE_BASE_MCP_PROCESS.kill()
#     _KNOWLEDGE_BASE_MCP_PROCESS = None

# def _start_knowledge_base_mcp_server():
#     global _KNOWLEDGE_BASE_MCP_PROCESS
#     if _KNOWLEDGE_BASE_MCP_PROCESS is not None and _KNOWLEDGE_BASE_MCP_PROCESS.poll() is None:
#         return
#     _KNOWLEDGE_BASE_MCP_PROCESS = subprocess.Popen(
#         [sys.executable, "knowledge_base_mcp.py"],
#         cwd=os.path.dirname(__file__),
#         env=os.environ.copy(),
#     )
#     atexit.register(_cleanup_knowledge_base_mcp_server)
#     for _ in range(20):
#         if _KNOWLEDGE_BASE_MCP_PROCESS.poll() is not None:
#             raise RuntimeError("知识库 MCP 服务启动失败。")
#         try:
#             response = requests.get("http://127.0.0.1:8000/mcp", timeout=0.5)
#             if response.status_code in (200, 400, 404, 405, 406):
#                 return
#         except Exception:
#             pass
#         time.sleep(0.2)
#     raise RuntimeError("知识库 MCP 服务启动超时。")

def _load_mcp_tools():
    # _start_knowledge_base_mcp_server()

    async def _load():
        client = MultiServerMCPClient(
            {
                "juhe_mcp": {
                    "transport": "sse",
                    "url": "https://mcp.juhe.cn/sse?token=LOtUYoDAXDf5bGZjTGESDO5w6NmCOXZcLnwqfxXvZcZVV6",
                },
                "knowledge_base": {
                    "transport": "streamable-http",
                    "url": "http://127.0.0.1:8000/mcp",
                },
            }
        )
        return await client.get_tools()

    return asyncio.run(_load())

def dxh_agent():
    openai_api_key = _get_openai_api_key()
    if not openai_api_key:
        raise ValueError("未找到 OPEN_AI_APIKEY，请检查根目录 .env 文件。")
    base_url = _get_openai_base_url()
    _configure_no_proxy_for_base_url(base_url)
    mcp_tools = _load_mcp_tools()
    agent = create_agent(
        model=ChatOpenAI(
            model="gpt-5-mini",
            base_url=base_url,
            api_key=openai_api_key,
        ),
        tools=[search_wikipedia, *mcp_tools],
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
    asyncio.run(run_astream(agent, user_message))
