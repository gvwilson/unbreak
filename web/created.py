import asyncio
import json

import httpx


async def app(scope, receive, send):
    assert scope["type"] == "http"
    event = await receive()
    body = json.loads(event.get("body", b"{}"))
    resource = {"id": 42, **body}
    await send({
        "type": "http.response.start",
        "status": 201,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({
        "type": "http.response.body",
        "body": json.dumps(resource).encode(),
    })


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/users", json={"name": "Alice"})
        # BUG: checks for exactly 200, but a successful POST returns 201 Created;
        # BUG: use r.is_success to accept any 2xx status code instead
        if r.status_code == 200:
            print("created:", r.json())
        else:
            print(f"request failed with status {r.status_code}")


asyncio.run(main())
