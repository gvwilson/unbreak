import asyncio

import httpx


async def app(scope, receive, send):
    assert scope["type"] == "http"
    await send({
        "type": "http.response.start",
        "status": 404,
        "headers": [(b"content-type", b"text/html")],
    })
    await send({
        "type": "http.response.body",
        "body": b"<html><body><h1>404 Not Found</h1></body></html>",
    })


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/data")
        # BUG: .json() is called without checking r.status_code first;
        # BUG: a 404 response contains HTML, not JSON, so this raises a JSONDecodeError
        data = r.json()
        print(data)


asyncio.run(main())
