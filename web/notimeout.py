import asyncio

import httpx

# Simulated server delay in seconds
SERVER_DELAY = 10


async def app(scope, receive, send):
    assert scope["type"] == "http"
    await asyncio.sleep(SERVER_DELAY)
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({"type": "http.response.body", "body": b'{"status": "done"}'})


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # BUG: timeout=None disables all timeouts; the call will wait indefinitely
        # BUG: for a slow or unresponsive server; use a finite timeout such as
        # BUG: httpx.Timeout(connect=5.0, read=5.0) to fail fast instead
        r = await client.get("/report", timeout=None)
        print(r.json())


asyncio.run(main())
