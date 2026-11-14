from fastapi import FastAPI, Form
import uvicorn

app = FastAPI()


@app.post("/register")
def register(username: str = Form(...), email: str = Form(...)):
    return {"username": username, "email": email}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
