from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

app = FastAPI()

# BUG: the router already declares prefix="/api", and include_router adds "/api"
# BUG: again; the actual registered path is /api/api/items, not /api/items;
# BUG: remove the prefix from one of the two places
router = APIRouter(prefix="/api")


@router.get("/items")
def get_items():
    return {"items": ["apple", "banana"]}


app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
