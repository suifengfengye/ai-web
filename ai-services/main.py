from fastapi import FastAPI, Path, Query, Body
import uvicorn
from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from fastapi.responses import StreamingResponse
from langchain_core.runnables.history import RunnableWithMessageHistory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder

# uvicorn APP [OPTIONS]
# uvicorn "<module>:<attribute>" [OPTIONS]
app = FastAPI()


class OpTypeEnum(Enum):
    empty = ""
    polish = "polish"
    continue_writing = "continue_writing"
    shorten = "shorten"
    expand = "expand"


class OpSubTypeEnum(Enum):
    empty = ""
    colloquial = "colloquial"
    lively = "lively"
    formal = "formal"


class AIDocBodyType(BaseModel):
    op_type: OpTypeEnum = Field(default=OpTypeEnum.empty, title="操作类型")
    op_sub_type: OpSubTypeEnum = Field(
        default=OpSubTypeEnum.empty, title="润色的子类型")
    question: str = Field(default="", description="自由问题")
    content: str = ""


def get_session_history(session_id: str):
    return SQLChatMessageHistory(session_id,
                                 connection=create_engine("sqlite:///./db/memory.db"))


def aget_session_history(session_id: str):
    return SQLChatMessageHistory(session_id,
                                 connection=create_async_engine(
                                     "sqlite+aiosqlite:///./db/memory.db"),
                                 async_mode=True)


@app.post("/ai_docs/generate")
async def generate_ai_docs(params: AIDocBodyType = Body(title="请求体信息")):
    """
        1. 润色 (polish)
          1.1 口语化 (colloquial)s
          1.2 更活泼 (lively)
          1.3 更正式 (formal)
        2. 续写 (continue_writing)
        3. 缩短篇幅 (shorten)
        4. 扩充篇幅 (expand)
      """
    # 1. 编写SystemPrompt
    system_prompt_text = ("你是一位著名的作家，名字叫做'费小V'。"
                          "如果问你'你是谁',请不要回答任何其他内容，直接回答'费小V'即可。"
                          "现在的任务是帮助用户将文章的内容进行处理，续写文章、缩短文章篇幅或者扩充文章篇幅。")
    # 2. 构建prompt对象
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt_text),
        MessagesPlaceholder(variable_name="history"),
        ('human', "{input}")
    ])
    # 3. 创建llm对象
    llm = ChatOllama(model="llama3")
    # 4. 构建langchain对象
    chain = prompt | llm
    # chain_history = RunnableWithMessageHistory(
    #     chain,
    #     get_session_history=get_session_history,
    #     history_messages_key="history"
    # )
    achain_history = RunnableWithMessageHistory(
        chain,
        get_session_history=aget_session_history,
        history_messages_key="history"
    )
    # 5. 编写业务逻辑
    input = ""
    if params.question:
        if params.content:
            input = ("根据用户的问题，对文章内容进行处理。"
                     f"问题='{params.question}'"
                     f"文章内容='{params.content}")
        else:
            input = params.question
    else:
        action_dict = {
            "polish": "润色",
            "continue_writing": "续写",
            "shorten": "缩短篇幅",
            "expand": "扩充篇幅",
        }
        sub_action_dict = {
            "colloquial": "更口语化",
            "lively": "更活泼",
            "formal": "更正式",
        }
        op_type_zh = action_dict[params.op_type.value]
        action = f"{op_type_zh}处理"
        if params.op_type == OpTypeEnum.polish:
            op_sub_type_zh = sub_action_dict[params.op_sub_type.value]
            action = f"润色处理,让文章内容{op_sub_type_zh}"
        input = f"请对下面的文章内容进行{action}:{params.content}"

    # 1 invoke()调用
    # result = chain_history.invoke({
    #     "input": input
    # }, {"configurable": {"session_id": "daxiaohan_01"}})
    # return result
    """
    {"input": input}
    {"configurable": {"session_id": "daxiaohan_01"}} 
    👇
    {"input": input, "history": [SystemMessage(content=""),HumanMessage(content=""),...]}
    👇
    prompt 👉 llm
    
    """

    # 2 stream()调用
    # result = chain.stream({
    #   "input": input
    # })
    # # AIMessageChunk(content="xxxx")
    # def stream_response(result):
    #   # yield 'xxxxx'
    #   for chunk in result:
    #     yield chunk.content
    # return StreamingResponse(stream_response(result), media_type="text/plain")

    # 3. ainvoke()调用
    # result = await chain.ainvoke({
    #   "input": input
    # })
    # return result

    # 4. astream()调用
    result = achain_history.astream({
        "input": input
    }, {"configurable": {"session_id": "daxiaohan_01"}})
    # AIMessageChunk(content="xxxx")

    async def astream_response(result):
        # yield 'xxxxx'
        async for chunk in result:
            yield chunk.content
    return StreamingResponse(astream_response(result), media_type="text/plain")


# python fastapi_demo.py
if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8081, reload=True)
