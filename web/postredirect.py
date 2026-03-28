import asyncio
import json

import httpx


async def app(scope, receive, send):
    assert scope["type"] == "http"
    if scope["path"] == "/submit":
        await send({
            "type": "http.response.start",
            "status": 302,
            "headers": [(b"location", b"http://test/result")],
        })
        await send({"type": "http.response.body", "body": b""})
    else:
        event = await receive()
        body = event.get("body", b"")
        msg = json.dumps({
            "method": scope["method"],
            "body": body.decode() if body else "(empty)",
        }, indent=2).encode()
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/json")],
        })
        await send({"type": "http.response.body", "body": msg})


async def main():
    payload = {"username": "alice", "password": "s3cr3t"}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # BUG: follow_redirects=True causes httpx to follow the 302 response,
        # BUG: but HTTP convention changes the method from POST to GET when following
        # BUG: a 302, so the request body (including credentials) is silently dropped
        r = await client.post("/submit", json=payload, follow_redirects=True)
        print(r.text)


asyncio.run(main())
