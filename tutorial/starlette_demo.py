from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn


async def homepage(request):
    return JSONResponse({'hello': 'world2'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])

if __name__ == '__main__':
    uvicorn.run("starlette_demo:app", host="127.0.0.1", port=8089, reload=True)
