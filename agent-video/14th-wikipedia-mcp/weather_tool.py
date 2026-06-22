from langchain.tools import tool
from dotenv import load_dotenv
import os
import requests

_ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(_ENV_PATH)

def _get_juhe_api_key() -> str | None:
    api_key = os.getenv("JUHE_API_KEY")
    if api_key:
        return api_key
    load_dotenv(_ENV_PATH, override=False)
    return os.getenv("JUHE_API_KEY")

@tool
def get_weather_forecast(city: str) -> str:
    """根据城市名称获取实时天气与未来预报。"""
    if not city or not city.strip():
        return "城市名称为空。"

    api_key = _get_juhe_api_key()
    if not api_key:
        return "未找到 JUHE_API_KEY，请检查根目录 .env 文件。"

    api_url = "http://apis.juhe.cn/simpleWeather/query"
    try:
        resp = requests.get(
            api_url,
            params={"key": api_key, "city": city.strip()},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        if data.get("error_code") != 0:
            reason = data.get("reason") or "未知错误"
            return f"天气查询失败：{reason}"

        result = data.get("result") or {}
        city_name = result.get("city") or city.strip()
        realtime = result.get("realtime") or {}
        future = result.get("future") or []

        lines: list[str] = [f"城市：{city_name}"]
        if realtime:
            realtime_parts = [
                f"温度 {realtime.get('temperature')}℃" if realtime.get("temperature") else None,
                f"湿度 {realtime.get('humidity')}%" if realtime.get("humidity") else None,
                realtime.get("info"),
                realtime.get("direct"),
                realtime.get("power"),
                f"空气质量 {realtime.get('aqi')}" if realtime.get("aqi") else None,
            ]
            realtime_text = "，".join([p for p in realtime_parts if p])
            if realtime_text:
                lines.append(f"实时：{realtime_text}")

        if future:
            lines.append("未来预报：")
            for item in future:
                date = item.get("date") or ""
                temperature = item.get("temperature") or ""
                weather = item.get("weather") or ""
                direct = item.get("direct") or ""
                parts = [p for p in [date, weather, temperature, direct] if p]
                if parts:
                    lines.append("- " + " ".join(parts))

        return "\n".join(lines)
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
            return f"天气查询失败（HTTP {status}）。{body}"
        return f"天气查询失败。{str(e)}"
    except Exception as e:
        return f"天气查询异常：{str(e)}"
