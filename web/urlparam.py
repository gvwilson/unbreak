import asyncio

import httpx


async def app(scope, receive, send):
    assert scope["type"] == "http"
    qs = scope.get("query_string", b"").decode()
    params = {}
    for pair in qs.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            params[k] = v
        elif pair:
            params[pair] = "(no value)"
    msg = f"parsed params: {params}".encode()
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({"type": "http.response.body", "body": msg})


async def main():
    category = "books&games"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # BUG: the & inside category is interpreted as a query-string separator,
        # BUG: so the server sees category="books" and a bare key "games" with no value;
        # BUG: use params={"category": category, "limit": "10"} to encode correctly
        r = await client.get(f"/items?category={category}&limit=10")
        print(r.text)


asyncio.run(main())
