import asyncio
import json

import httpx

ALL_RECORDS = [{"id": i, "value": i * 10} for i in range(1, 21)]
PAGE_SIZE = 5


async def app(scope, receive, send):
    assert scope["type"] == "http"
    qs = scope.get("query_string", b"").decode()
    params = dict(p.split("=", 1) for p in qs.split("&") if "=" in p)
    page = int(params.get("page", "1"))
    start = (page - 1) * PAGE_SIZE
    items = ALL_RECORDS[start : start + PAGE_SIZE]
    next_page = page + 1 if start + PAGE_SIZE < len(ALL_RECORDS) else None
    body = json.dumps({"items": items, "next_page": next_page}).encode()
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({"type": "http.response.body", "body": body})


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # BUG: only fetches page 1 and ignores next_page in the response,
        # BUG: so only 5 of 20 records are retrieved without any error or warning
        r = await client.get("/records?page=1")
        data = r.json()
        print(f"retrieved {len(data['items'])} records")
        print(f"next_page field in response: {data['next_page']!r}")
        print(f"total records on server: {len(ALL_RECORDS)}")


asyncio.run(main())
