from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()


# BUG: await request.body() reads and exhausts the request stream;
# BUG: when the route handler calls request.body() again it gets b"",
# BUG: an empty bytes object, because the stream has already been consumed;
# BUG: fix by caching: set request._body = body after reading in the middleware
@app.middleware("http")
async def log_body(request: Request, call_next):
    body = await request.body()
    print(f"  middleware read: {body!r}")
    return await call_next(request)


@app.post("/echo")
async def echo(request: Request):
    body = await request.body()
    return {"received": body.decode()}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
