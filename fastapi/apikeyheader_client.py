import httpx

# BUG: the client makes a request with no x-api-key header and expects a 401,
# BUG: but the server's dependency never raises 401, so the request succeeds
# BUG: and the secret is returned to anyone
r = httpx.get("http://localhost:8000/protected")
print("status:", r.status_code)
print("body:", r.json())
