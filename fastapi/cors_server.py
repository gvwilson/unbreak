from fastapi import FastAPI
import uvicorn

app = FastAPI()


# BUG: no CORSMiddleware is added; the server never sends
# BUG: "Access-Control-Allow-Origin" in its responses, so any browser
# BUG: or client that enforces CORS will block the response even when
# BUG: the server returns 200; add fastapi.middleware.cors.CORSMiddleware
@app.get("/data")
def get_data():
    return {"value": 42}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
