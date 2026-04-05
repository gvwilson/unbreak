import asyncio
import json

import httpx

_request_count = 0


async def app(scope, receive, send):
    global _request_count
    assert scope["type"] == "http"
    _request_count += 1
    await send({
        "type": "http.response.start",
        "status": 429,
        "headers": [
            (b"content-type", b"application/json"),
            (b"retry-after", b"60"),
        ],
    })
    await send({
        "type": "http.response.body",
        "body": json.dumps({"error": "rate limit exceeded"}).encode(),
    })


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        for attempt in range(1, 4):
            r = await client.get("/api/data")
            if r.status_code == 200:
                print("success:", r.json())
                break
            # BUG: retries without checking for 429 or reading the Retry-After header;
            # BUG: should check r.status_code == 429 and wait int(r.headers["retry-after"])
            # BUG: seconds before the next attempt
            print(f"attempt {attempt}: status {r.status_code}, retry-after={r.headers.get('retry-after')!r}")
    print(f"total requests sent: {_request_count}")


asyncio.run(main())
