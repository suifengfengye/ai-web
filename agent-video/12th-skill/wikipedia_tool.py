from langchain.tools import tool
from urllib.parse import quote
import requests


@tool
def search_wikipedia(query: str, language_code: str = "zh", limit: int = 3) -> str:
    """在 Wikipedia 中搜索相关词条并返回最匹配词条的完整内容。"""
    if not query or not query.strip():
        return "查询内容为空。"

    base_url = "https://api.wikimedia.org/core/v1/wikipedia"
    endpoint = f"/{language_code}/search/page"
    headers = {"User-Agent": "DXH_APP"}

    try:
        resp = requests.get(
            f"{base_url}{endpoint}",
            headers=headers,
            params={"q": query.strip(), "limit": max(1, min(limit, 10))},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        pages = data.get("pages") or []
        if not pages:
            return "Wikipedia 未检索到相关内容。"

        page = pages[0] or {}
        title = page.get("title") or page.get("key") or ""
        key = page.get("key") or title
        if not key:
            return "Wikipedia 检索结果缺少词条信息。"
        excerpt = page.get("excerpt") or ""
        if not excerpt:
            return "Wikipedia 检索结果缺少内容摘要。"
        return f"标题：{title or key}\n内容摘要：{excerpt}"
        # html_url = f"{base_url}/{language_code}/page/{quote(key)}/html"
        # html_resp = requests.get(html_url, headers=headers, timeout=60)
        # html_resp.raise_for_status()
        # html_content = (html_resp.text or "").strip()
        # if not html_content:
        #     return "Wikipedia 词条内容为空。"

        # display_url = f"https://{language_code}.wikipedia.org/wiki/{quote(key)}"
        # return f"标题：{title or key}\n链接：{display_url}\n\n{html_content}"
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
            return f"Wikipedia 请求失败（HTTP {status}）。{body}"
        return f"Wikipedia 请求失败。{str(e)}"
    except Exception as e:
        return f"Wikipedia 检索异常：{str(e)}"
