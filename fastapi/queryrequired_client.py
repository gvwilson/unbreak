import httpx

# BUG: the /search endpoint requires a "category" query parameter;
# BUG: omitting it causes the server to return 422 Unprocessable Entity,
# BUG: not 200, so r.json() contains an error dict, not search results
r = httpx.get("http://localhost:8000/search")
print("status:", r.status_code)
print(r.json())
