from time import sleep
from langchain.tools import tool
from dotenv import load_dotenv
import os
import requests
from langgraph.config import get_stream_writer

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
    """使用聚合数据天气 API 查询指定城市的实时与未来天气。"""
    if not city or not city.strip():
        return "城市为空，请输入需要查询的城市名称。"

    api_key = _get_juhe_api_key()
    if not api_key:
        return "未找到 JUHE_API_KEY，请检查根目录 .env 文件。"

    api_url = "http://apis.juhe.cn/simpleWeather/query"
    request_params = {"key": api_key, "city": city.strip()}

    try:
        response = requests.get(api_url, params=request_params, timeout=30)
        response.raise_for_status()
        data = response.json() if response.content else {}
        if data.get("error_code") != 0:
            reason = data.get("reason") or "天气查询失败。"
            return f"天气查询失败：{reason}"

        result = data.get("result") or {}
        city_name = result.get("city") or city.strip()
        realtime = result.get("realtime") or {}
        future = result.get("future") or []

        lines: list[str] = [f"城市：{city_name}"]
        if realtime:
            lines.append("实时天气：")
            temperature = realtime.get("temperature")
            info = realtime.get("info")
            humidity = realtime.get("humidity")
            direct = realtime.get("direct")
            power = realtime.get("power")
            aqi = realtime.get("aqi")
            realtime_parts = []
            if temperature:
                realtime_parts.append(f"温度 {temperature}℃")
            if info:
                realtime_parts.append(f"天气 {info}")
            if humidity:
                realtime_parts.append(f"湿度 {humidity}%")
            if direct or power:
                realtime_parts.append(f"风向风力 {direct or ''}{power or ''}".strip())
            if aqi:
                realtime_parts.append(f"AQI {aqi}")
            if realtime_parts:
                lines.append(" - " + "，".join(realtime_parts))

        if future:
            lines.append("未来天气：")
            for day in future[:5]:
                date = day.get("date") or ""
                temperature = day.get("temperature") or ""
                weather = day.get("weather") or ""
                direct = day.get("direct") or ""
                detail_parts = [p for p in [weather, temperature, direct] if p]
                if date and detail_parts:
                    lines.append(f" - {date}：{'，'.join(detail_parts)}")
        # 体验流式输出
        # writer = get_stream_writer()
        # msg = "\n".join(lines) if len(lines) > 1 else "未获取到天气信息。"
        # for char in msg:
        #     writer(char)
        #     sleep(0.2)
        return "\n".join(lines) if len(lines) > 1 else "未获取到天气信息。"
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
            return f"天气请求失败（HTTP {status}）。{body}"
        return f"天气请求失败。{str(e)}"
    except Exception as e:
        return f"天气查询异常：{str(e)}"
