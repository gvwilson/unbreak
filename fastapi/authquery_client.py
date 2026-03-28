import httpx

API_KEY = "s3cr3t"

# BUG: the API key is passed as a URL query parameter; it appears in the
# BUG: full URL that server access logs record, in browser history, and in
# BUG: any proxy logs between client and server; pass it in a header instead:
# BUG: headers={"Authorization": f"Bearer {API_KEY}"}
r = httpx.get("http://localhost:8000/data", params={"api_key": API_KEY})
print("status:", r.status_code)
print("URL sent (check for the key):", r.request.url)
