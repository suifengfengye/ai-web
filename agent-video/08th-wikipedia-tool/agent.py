from langchain.agents import create_agent, AgentState
from langchain_openai import ChatOpenAI
from prompts import system_prompt
from langchain.tools import tool
from wikipedia_tool import search_wikipedia
from dotenv import load_dotenv
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
        tools=[search_dify_knowledge_base, search_wikipedia],
        system_prompt=system_prompt,
    )
    return agent

if __name__ == "__main__":
    agent = dxh_agent()
    print("开始调用....")
    result = agent.invoke({
        "messages" : [
            {"role": "user", "content": "请你提供一份广州3天的旅游攻略，出行时间为2026.1.1到2026.1.3"}
        ]
    })
    print(result)
    print("调用结束!!!")
