from fastapi import FastAPI
import uvicorn

# uvicorn APP [OPTIONS]
# uvicorn "<module>:<attribute>" [OPTIONS]
app = FastAPI()

@app.get("/")
async def main():
  return {"message": "Hello FastAPI OK!"}

@app.post("/ai_docs/create")
async def create_docs():
  ...

@app.put("/ai_docs/update")
async def update_docs():
  ...

@app.delete("/ai_docs/delete")
async def delete_docs():
  ...

# python fastapi_demo.py
if __name__ == '__main__':
  uvicorn.run('fastapi_demo:app', host="127.0.0.1", port=8081, reload=True)
