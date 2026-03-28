import httpx

r = httpx.post("http://localhost:8000/items", params={"name": "widget"})
if r.status_code == 201:
    print("created:", r.json())
else:
    print(f"request failed with status {r.status_code}: {r.text}")
