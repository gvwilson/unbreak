import httpx

# BUG: the /orders endpoint declares a Pydantic body model and expects JSON in the body;
# BUG: params= puts data in the URL query string, which FastAPI ignores for body fields,
# BUG: so the required fields are missing and the server returns 422; use json= instead
r = httpx.post(
    "http://localhost:8000/orders",
    params={"product": "widget", "quantity": 3},
)
print("status:", r.status_code)
print(r.json())
