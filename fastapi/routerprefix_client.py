import httpx

for path in ["/api/items", "/api/api/items"]:
    r = httpx.get(f"http://localhost:8000{path}")
    print(f"GET {path}: status={r.status_code}  body={r.text[:60]}")
