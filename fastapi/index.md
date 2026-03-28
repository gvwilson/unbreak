# FastAPI

FastAPI is a Python framework for building web APIs.
You describe each endpoint as a function, annotate its parameters with types,
and FastAPI handles routing, validation, and serialization automatically.
Each exercise here uses two files: a server and a client.
Open one terminal, start the server with `uv run <slug>_server.py`,
then open a second terminal and run the client with `uv run <slug>_client.py`.
Read both files before deciding where the bug is.

## Check whether a new resource was created {: #fastapi-wrongstatus}

Start the server, run the client, and read the output.
The client says the request failed, but did it?
Check the server terminal for any error messages.

[% inc wrongstatus_server.py scrub="\s*# BUG.*" %]

[% inc wrongstatus_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `status_code=201` argument on the `@app.post` decorator.
FastAPI defaults to `200 OK` for every route.
A POST that creates a resource should return `201 Created`,
and the client correctly checks for `201`, so the check fails
even though the item was created.

Shows: the range of 2xx status codes, when each is appropriate, and how to
set a non-default status with `@app.post("/items", status_code=201)`.

To find it: print `r.status_code` in the client.
If it prints `200` for a creation endpoint,
check the decorator for a missing `status_code=201` argument.

</details>

## Retrieve an item by its identifier {: #fastapi-pathtype}

Start the server, run the client, and read the output.
Every item comes back as "not found" even though the items exist.
What type does the server use to look up items?

[% inc pathtype_server.py scrub="\s*# BUG.*" %]

[% inc pathtype_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is declaring `item_id: str` in the route function.
FastAPI parses the path segment and passes a string to the handler,
but `ITEMS` uses integer keys.
The expression `"3" in ITEMS` is always `False` because `"3" != 3`.

Shows: how FastAPI's type annotations do more than document—they control
parsing; changing `str` to `int` makes FastAPI convert the path segment
before calling the handler.

To find it: add `print(type(item_id), item_id, type(list(ITEMS.keys())[0]))` at
the top of the handler.
If the types differ, the annotation is wrong.

</details>

## Search a catalogue with a required filter {: #fastapi-queryrequired}

Start the server, run the client, and read the output.
The client prints a status code and a response body: are either what you expected?

[% inc queryrequired_server.py %]

[% inc queryrequired_client.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is omitting the `category` query parameter in the client.
FastAPI treats any function parameter that is not a path parameter and has
no default value as a required query parameter.
When the parameter is absent the server returns `422 Unprocessable Entity`
with a JSON body describing the validation error.

Shows: how FastAPI validates incoming requests before calling the handler,
and how to give a parameter a default value (`category: str = ""`) to make
it optional.

To find it: print `r.status_code`.
A `422` means the request was malformed.
The `r.json()["detail"]` list names each missing or invalid field.

</details>

## Update the price of an existing item {: #fastapi-putpatch}

Start the server, run the client, and compare the "before" and "after" output.
Which fields changed that you did not intend to change?

[% inc putpatch_server.py %]

[% inc putpatch_client.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using PUT with a partial body.
PUT replaces the entire resource with the supplied body.
Any field not included in the request resets to its model default,
so `price` goes from `9.99` to `0.0` and `in_stock` stays `True` only
by coincidence; the original value is gone.

Shows: the semantic difference between PUT (full replacement) and PATCH
(partial update), and why sending only the fields you want to change requires
a PATCH endpoint that merges the incoming data with the stored record.

To find it: fetch and print the item before and after.
If fields you did not mention in the request body have changed,
PUT replaced the whole resource.

</details>

## Place an order through the API {: #fastapi-bodyasquery}

Start the server, run the client, and read the output.
The server returns an error even though the client sends the right data.
Where in the HTTP request does the data actually end up?

[% inc bodyasquery_server.py %]

[% inc bodyasquery_client.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `params=` in the POST call.
`params=` appends key-value pairs to the URL query string.
The server declares an `Order` Pydantic model, which tells FastAPI to look
for a JSON body, not query parameters.
Because the body is empty, FastAPI returns `422 Unprocessable Entity`.

Shows: the difference between `params=` (query string), `data=` (form body),
and `json=` (JSON body), and how to read the full request URL to confirm
where data was sent.

To find it: print `str(r.request.url)`.
If the product and quantity appear after a `?` in the URL,
the data was sent as query parameters.
Change `params=` to `json=`.

</details>

## Navigate to a form for creating new items {: #fastapi-routeorder}

Start the server, run the client, and read the response.
Which route actually handled the request?

[% inc routeorder_server.py scrub="\s*# BUG.*" %]

[% inc routeorder_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is declaring the parameterized route `/items/{item_id}` before the
static route `/items/new`.
FastAPI registers routes in the order they appear in the source and stops
at the first match, so the string `"new"` is captured as `item_id` and the
`/items/new` handler is never reached.

Shows: how route registration order matters in FastAPI and why specific routes
must be declared before parameterized ones that could absorb them.

To find it: move `@app.get("/items/new")` above `@app.get("/items/{item_id}")`
and rerun the client.

</details>

## Serve slow and fast endpoints concurrently {: #fastapi-asyncblocking}

Start the server, run the client, and read the elapsed time.
Both requests are sent almost simultaneously, so why does the fast one wait?

[% inc asyncblocking_server.py scrub="\s*# BUG.*" %]

[% inc asyncblocking_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `time.sleep()` inside an `async def` route.
`time.sleep()` is a blocking call that holds the CPU and prevents the event
loop from running any other coroutine.
While `/slow` is sleeping, `/fast` cannot be handled until the sleep finishes,
even though it only needs a microsecond.

Shows: the difference between blocking (`time.sleep`) and non-blocking
(`asyncio.sleep`) waits, and why blocking code in an async route defeats
the concurrency model.

To find it: replace `time.sleep(2)` with `await asyncio.sleep(2)` and rerun
the client.
The elapsed time will drop to just over 2 seconds and `/fast` will respond
immediately.

</details>

## Count requests to an endpoint {: #fastapi-startupstate}

Start the server, run the client five times in a row, and read the output.
What value does the counter hold on every call?

[% inc startupstate_server.py scrub="\s*# BUG.*" %]

[% inc startupstate_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is initializing `counter = 0` inside the route handler.
Python re-executes the assignment on every request, so the counter always
starts at zero and is incremented to one before being returned.
It never accumulates across calls.

Shows: the difference between module-level state (created once when the
module loads) and function-local state (created fresh on every call).

To find it: move `counter = 0` to module level (outside the function) and
declare it `global` inside the handler before modifying it.
The counter will then persist between requests.

</details>

## Look up an item that may not exist {: #fastapi-noexcept}

Start the server, run the client, and compare the status codes for item 1 and item 99.
What does item 99's response look like?

[% inc noexcept_server.py scrub="\s*# BUG.*" %]

[% inc noexcept_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is returning the result of `dict.get()` directly.
When `item_id` is not in `ITEMS`, `get()` returns `None`,
and FastAPI serializes `None` as the JSON literal `null` with a `200 OK`
status code.
A client has no way to distinguish "found, value is null" from "not found".

Shows: how to raise `HTTPException(status_code=404, detail="not found")` so
FastAPI returns a proper `404 Not Found` response with a JSON error body.

To find it: check `r.status_code` for the missing item.
If it is `200` with body `null`, the handler returned `None` instead of
raising an exception.

</details>

## Allow a browser on another origin to call the API {: #fastapi-cors}

Start the server, run the client, and read the output.
Which header is missing from the response, and why does that matter for browsers?

[% inc cors_server.py scrub="\s*# BUG.*" %]

[% inc cors_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is missing CORS middleware.
Browsers enforce the Same-Origin Policy: a page at `http://example.com` may
not read a response from `http://localhost:8000` unless the server includes
an `Access-Control-Allow-Origin` header granting permission.
Without `CORSMiddleware`, FastAPI never sends that header and any browser
making the request will block the response.

Shows: how to add `CORSMiddleware` with `allow_origins`, `allow_methods`, and
`allow_headers`, and why the `Origin` header in the client request triggers
the CORS check.

To find it: add `from fastapi.middleware.cors import CORSMiddleware` and call
`app.add_middleware(CORSMiddleware, allow_origins=["*"])`.
Rerun the client and confirm the `Access-Control-Allow-Origin` header now
appears.

</details>

## Submit an item with its price {: #fastapi-extrafields}

Start the server, run the client, and read the response.
What price did the server record?
Is it what the client sent?

[% inc extrafields_server.py %]

[% inc extrafields_client.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a typo: `"prise"` instead of `"price"`.
Pydantic's default behaviour is to ignore extra fields it does not recognise,
so the misspelled key is silently discarded.
`price` has a default of `0.0`, so the server receives `price=0.0` with no
error or warning.

Shows: how to configure Pydantic to reject unknown fields with
`model_config = ConfigDict(extra="forbid")`, which would turn this silent
data-loss into an immediate `422` error.

To find it: compare the keys you sent (`prise`) against the model's field
names (`price`).
If you set `extra="forbid"` in the model config, Pydantic raises the error
for you automatically.

</details>

## Return an item with its tracking code {: #fastapi-responsemodel}

Start the server, run the client, and read the response.
Which field is missing from the response even though you sent it in the request?

[% inc responsemodel_server.py scrub="\s*# BUG.*" %]

[% inc responsemodel_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `ItemOut` does not include `internal_code`.
`response_model=ItemOut` tells FastAPI to filter every response through that
schema before sending it.
Any field in the return value that is not declared in `ItemOut` is silently
dropped with no error and no warning.

Shows: how `response_model` controls the output schema independently of the
input schema, and how to include a field in the response model when clients
need it.

To find it: add `internal_code: str` to `ItemOut` and rerun the client.
The field will appear in the response.

</details>

## Fetch protected data with an API key {: #fastapi-authquery}

Start the server, run the client, and look at the URL the client actually sent.
Where does the secret appear?

[% inc authquery_server.py %]

[% inc authquery_client.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is putting the API key in the URL query string with `params=`.
The full URL, including the key, is recorded in every server access log,
stored in browser history, and forwarded by HTTP proxies.
A key that appears in URLs is not secret for long.

Shows: how to send credentials in an `Authorization` header
(`headers={"Authorization": f"Bearer {API_KEY}"}`) where they are kept out
of logs and not cached by browsers.

To find it: print `str(r.request.url)`.
If the secret appears after `?api_key=`, it will be logged.
Switch to a header.

</details>

## Log the body of every incoming request {: #fastapi-middleware}

Start the server, run the client, and compare what the middleware prints to what
the route handler returns.
Are they the same?

[% inc middleware_server.py scrub="\s*# BUG.*" %]

[% inc middleware_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `await request.body()` in the middleware without caching
the result.
`request.body()` reads from the underlying stream, which can only be consumed
once.
When the route handler calls `request.body()` it gets back `b""` because
the stream is exhausted.

Shows: how to cache the body after reading it with
`request._body = body` so the stream appears to be re-readable by downstream
handlers.

To find it: add a print of `await request.body()` inside the route and compare
it with what the middleware printed.
If the route sees an empty body while the middleware saw the real one, the
stream was consumed and not cached.

</details>

## List all items through the API router {: #fastapi-routerprefix}

Start the server, run the client, and read the status codes.
Which path actually works?

[% inc routerprefix_server.py scrub="\s*# BUG.*" %]

[% inc routerprefix_client.py %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is setting `prefix="/api"` in both the `APIRouter` constructor and the
`include_router` call.
FastAPI concatenates the two prefixes, so the registered path is
`/api/api/items` rather than `/api/items`.
The intended path returns `404` while the doubled path returns `200`.

Shows: how FastAPI builds full paths by joining the app's base, the
`include_router` prefix, and the router's own prefix, and why a prefix should
appear in only one of those two places.

To find it: call `print([r.path for r in app.routes])` after the
`include_router` call and before `uvicorn.run`.
The registered path will show the duplication.

</details>
