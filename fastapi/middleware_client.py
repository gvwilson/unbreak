import httpx

r = httpx.post("http://localhost:8000/echo", content=b"hello world")
print("status:", r.status_code)
print("response:", r.json())
