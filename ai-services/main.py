from fastapi import FastAPI, Path
import uvicorn
from typing import Annotated
from enum import Enum

# uvicorn APP [OPTIONS]
# uvicorn "<module>:<attribute>" [OPTIONS]
app = FastAPI()

class OpTypeEnum(Enum):
  polish = "polish"
  continue_writing = "continue_writing"
  shorten = "shorten"
  expand = "expand"

class OpSubTypeEnum(Enum):
  colloquial = "colloquial"
  lively = "lively"
  formal = "formal"

@app.get("/ai_docs/{op_type}/{op_sub_type}")
async def generate_ai_docs(
  op_type: Annotated[OpTypeEnum, Path(
    title="文档操作类型", 
    description="文档操作类型",
    # max_length=10, 
    # min_length=2,
    # pattern=r"^(polish|continue_writing|shorten|expand)$"
    )], 
  op_sub_type: Annotated[OpSubTypeEnum, Path(title="润色的子操作", description="润色的子操作")]):
  """
      1. 润色 (polish)
        1.1 口语化 (colloquial)
        1.2 更活泼 (lively)
        1.3 更正式 (formal)
      2. 续写 (continue_writing)
      3. 缩短篇幅 (shorten)
      4. 扩充篇幅 (expand)
    """
  return {"message": f"op_type: {op_type.name},{op_type.value}, op_sub_type: {op_sub_type.name},{op_sub_type.value}"}


# python fastapi_demo.py
if __name__ == '__main__':
  uvicorn.run('main:app', host="127.0.0.1", port=8081, reload=True)
