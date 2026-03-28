import httpx

for item_id in [1, 2, 3]:
    r = httpx.get(f"http://localhost:8000/items/{item_id}")
    print(f"item {item_id}: {r.json()}")
