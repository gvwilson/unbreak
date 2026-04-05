import asyncio
import json

import httpx

# Server-side resource state
_resource = {"name": "Alice", "email": "alice@example.com", "role": "admin"}


async def app(scope, receive, send):
    assert scope["type"] == "http"
    event = await receive()
    if scope["method"] == "PUT":
        update = json.loads(event.get("body", b"{}"))
        # PUT replaces the entire resource with the request body
        _resource.clear()
        _resource.update(update)
    body = json.dumps(_resource, indent=2).encode()
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({"type": "http.response.body", "body": body})


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/user/1")
        print("before:", r.text)
        # BUG: PUT with only the name field replaces the whole resource,
        # BUG: wiping email and role; use PATCH to update only the specified fields
        r = await client.put("/user/1", json={"name": "Alicia"})
        print("after:", r.text)


asyncio.run(main())
