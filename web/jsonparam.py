import asyncio

import httpx


async def app(scope, receive, send):
    assert scope["type"] == "http"
    event = await receive()
    headers = dict(scope["headers"])
    content_type = headers.get(b"content-type", b"(not set)").decode()
    body = event.get("body", b"")
    msg = f"content-type: {content_type}\nbody: {body!r}".encode()
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({"type": "http.response.body", "body": msg})


async def main():
    payload = {"name": "Alice", "score": 95}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # BUG: data= sends a form-encoded body with content-type application/x-www-form-urlencoded;
        # BUG: use json= to send a JSON body with content-type application/json
        r = await client.post("/submit", data=payload)
        print(r.text)


asyncio.run(main())
