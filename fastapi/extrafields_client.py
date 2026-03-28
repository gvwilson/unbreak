import httpx

# BUG: "prise" is a misspelling of "price"; Pydantic's default behaviour is
# BUG: to silently ignore unknown fields, so the server receives price=0.0
# BUG: (the model default) and no error is raised; the intended price is lost
r = httpx.post(
    "http://localhost:8000/items",
    json={"name": "widget", "prise": 9.99},
)
print(r.json())
