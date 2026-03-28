import httpx

r = httpx.get(
    "http://localhost:8000/data",
    headers={"Origin": "http://example.com"},
)
print("status:", r.status_code)
allow = r.headers.get("access-control-allow-origin", "(missing)")
print("Access-Control-Allow-Origin:", allow)
if allow == "(missing)":
    print("A browser making a cross-origin request would block this response.")
