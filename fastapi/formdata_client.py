import httpx

# BUG: the server declares the fields with Form(...), so it expects form-encoded
# BUG: data, but the client sends a JSON body with json=; FastAPI can't find the
# BUG: form fields and returns 422; use data={"username": ..., "email": ...}
r = httpx.post(
    "http://localhost:8000/register",
    json={"username": "alice", "email": "alice@example.com"},
)
print("status:", r.status_code)
print("body:", r.text)
