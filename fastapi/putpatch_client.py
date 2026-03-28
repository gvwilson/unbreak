import httpx

r = httpx.get("http://localhost:8000/items/1")
print("before:", r.json())

# BUG: PUT replaces the entire resource with the supplied body;
# BUG: fields not included in the request reset to their model defaults,
# BUG: so price goes to 0.0 and in_stock goes to True even though we only
# BUG: wanted to rename the item; use PATCH and send only the changed fields
r = httpx.put("http://localhost:8000/items/1", json={"name": "widget v2"})
print("after: ", r.json())
