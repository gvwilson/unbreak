import httpx

r = httpx.get("http://localhost:8000/items/new")
print(r.json())
