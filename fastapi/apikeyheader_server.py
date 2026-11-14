from fastapi import FastAPI, Header, Depends, HTTPException
import uvicorn

app = FastAPI()

SECRET = "s3cr3t"


def require_api_key(x_api_key: str = Header(default=None)):
    # BUG: this dependency should reject requests whose x-api-key header is
    # BUG: missing or wrong by raising HTTPException(status_code=401), but it
    # BUG: does nothing, so the protected endpoint below runs for anyone
    pass


@app.get("/protected")
def protected(key: str = Depends(require_api_key)):
    return {"secret": "the answer is 42"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
