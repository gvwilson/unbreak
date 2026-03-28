import asyncio

import httpx


async def app(scope, receive, send):
    assert scope["type"] == "http"
    qs = scope.get("query_string", b"").decode()
    headers = dict(scope["headers"])
    auth = headers.get(b"authorization", b"(not set)").decode()
    msg = f"query string : {qs!r}\nauthorization: {auth!r}".encode()
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({"type": "http.response.body", "body": msg})


async def main():
    API_KEY = "secret-key-12345"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # BUG: the API key appears in the query string, which is recorded in server
        # BUG: logs, browser history, and any intermediate proxies; pass it in a
        # BUG: header instead: headers={"Authorization": f"Bearer {API_KEY}"}
        r = await client.get(f"/data?api_key={API_KEY}")
        print(r.text)


asyncio.run(main())
