import httpx

for item_id in [1, 99]:
    r = httpx.get(f"http://localhost:8000/items/{item_id}")
    print(f"item {item_id}: status={r.status_code}  body={r.text!r}")
