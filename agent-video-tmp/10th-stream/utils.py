from langchain_mcp_adapters.callbacks import CallbackContext
from mcp.types import LoggingMessageNotificationParams

async def on_progress(
    progress: float,
    total: float | None,
    message: str | None,
    context: CallbackContext
):
    """Handle progress updates from MCP servers."""
    percent = (progress / total * 100) if total else progress
    tool_name = context.tool_name if context.tool_name else ""
    print(f"###progress### [{context.server_name} - {tool_name}]:{percent:.2f}% - {message}")

async def on_logging_message(
    params: LoggingMessageNotificationParams,
    context: CallbackContext,
):
    tool_name = context.tool_name if context.tool_name else ""
    print(f"###logging### [{context.server_name} - {tool_name}] {params.level} : {params.data}")