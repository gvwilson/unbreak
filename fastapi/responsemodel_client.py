import httpx

r = httpx.post(
    "http://localhost:8000/items",
    json={"name": "widget", "price": 9.99, "internal_code": "W-42"},
)
data = r.json()
print("response:", data)
print("internal_code:", data.get("internal_code", "(missing)"))
