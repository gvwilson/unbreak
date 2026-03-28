import asyncio
import time

import httpx


async def main():
    async with httpx.AsyncClient() as client:
        start = time.monotonic()
        slow_task = asyncio.create_task(client.get("http://localhost:8000/slow"))
        await asyncio.sleep(0.1)
        fast_task = asyncio.create_task(client.get("http://localhost:8000/fast"))
        slow_r, fast_r = await asyncio.gather(slow_task, fast_task)
        elapsed = time.monotonic() - start
        print(f"/slow: {slow_r.json()}  /fast: {fast_r.json()}")
        print(f"total elapsed: {elapsed:.1f}s (expect ~2s if event loop was blocked)")


asyncio.run(main())
