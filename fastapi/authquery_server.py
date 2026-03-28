from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

SECRET = "s3cr3t"


@app.get("/data")
def get_data(request: Request, api_key: str = ""):
    if api_key != SECRET:
        return {"error": "unauthorized"}
    print(f"  request URL logged by server: {request.url}")
    return {"value": 42}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
