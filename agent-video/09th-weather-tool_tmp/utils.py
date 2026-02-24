# 1. tool_call_chunk: id, index: 0/1..., type: "tool_call_chunk",  取：tool_call_chunks字段
# 2. tools的响应: content,name,id,tool_call_id(对应tool_call的id，由这个ID建立对应关系)
# 3. 最终响应：content,id

"""
metadata:
- langgraph_step: 1/2...
- langgraph_node: model/tools/
- langgraph_triggers: ???
- langgraph_path: ???
- langgraph_checkpoint_ns: ???
- checkpoint_ns:???
- ls_provider: openai,模型提供商
- ls_model_name： 模型名称
- ls_model_type: chat ???
- ls_temperature: ???
"""

from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage

def render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)

def render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(message.tool_calls)
    if isinstance(message, ToolMessage):
        print(message.content_blocks)

