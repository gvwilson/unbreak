import httpx

for i in range(5):
    r = httpx.get("http://localhost:8000/count")
    print(f"call {i + 1}: {r.json()}")
