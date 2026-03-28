# HTMX

HTMX lets you add dynamic behavior to HTML pages by putting attributes directly on elements
rather than writing JavaScript. Each attribute tells the browser when to make a request,
where to send it, and which part of the page to update with the response.
Before trying any of these examples, start the server:

```
uv run server.py
```

Then open `http://localhost:8000` in a browser to see the list of examples,
or navigate directly to `http://localhost:8000/<slug>` for the one you want.

## Load data into a display panel {: #htmx-wrongswap}

Start the server, open the page, and click Load twice.
Does it keep working after the first click?

[% inc wrongswap.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `hx-swap="outerHTML"` combined with `hx-target="#panel"`. The first click
replaces the entire `<div id="panel">` element with the server's response `<p>Result: 42</p>`.
That `<p>` has no `id` attribute, so after the swap `#panel` no longer exists in the DOM.
The second click finds no target and silently does nothing.

Shows: the difference between `innerHTML` (replace the contents of the target, leaving
the element itself in place) and `outerHTML` (replace the target element entirely).

To find it: open DevTools, click Load once, then inspect the DOM. If the `<div id="panel">`
is gone and a bare `<p>` has taken its place, `outerHTML` swapped out the target itself.
Change `hx-swap="outerHTML"` to `hx-swap="innerHTML"` so the element stays in the DOM
and the next click can still find it.

</details>

## Show search results on a page {: #htmx-notarget}

Start the server, open the page, and click Search.
Where do the results appear?

[% inc notarget.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `hx-target` attribute. When no target is specified, HTMX defaults
to swapping the response into the element that triggered the request — the button itself.
The button's label is replaced by the results HTML, and the `<div id="results">` below
it stays empty.

Shows: HTMX's default target behavior and how to use `hx-target` to direct a response
to the correct element.

To find it: inspect the button in DevTools after clicking. If its content has changed to
a list of results, the response was swapped into the wrong element. Add
`hx-target="#results"` to the button so the response lands in the dedicated container.

</details>

## Display a loading message during a slow fetch {: #htmx-indicator}

Start the server, click Fetch, and watch the page during the two-second delay.
Does any loading message appear?

[% inc indicator.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `hx-indicator="#spinner"` pointing to an element that does not exist.
The `<span>` on the page has `id="loading"`, not `id="spinner"`. HTMX looks for
`#spinner` at request time, finds nothing, and never toggles visibility.

Shows: how `hx-indicator` works (HTMX adds `htmx-request` to the element during the
request, which the CSS rule converts to `display: inline`) and why element IDs must match
exactly.

To find it: open DevTools and search the DOM for an element with `id="spinner"`. If none
exists, the indicator selector is wrong. Change `hx-indicator="#spinner"` to
`hx-indicator="#loading"` to match the actual element.

</details>

## Filter a list as the user types {: #htmx-trigger}

Start the server and watch its terminal output while you type a five-letter word
one character at a time. How many requests arrive for each character?

[% inc trigger.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `hx-trigger="input"`, which fires a new request on every single keystroke.
Typing "apple" sends five requests in rapid succession. Each one may cancel the previous
before the user finishes typing, and each one adds server load for a query that will
be superseded immediately.

Shows: HTMX trigger modifiers and why a debounce delay matters for search-as-you-type.

To find it: watch the server log. If a request fires for every character, the trigger
has no debounce. Change `hx-trigger="input"` to
`hx-trigger="input changed delay:500ms"` to wait until the user pauses before sending.

</details>

## Search using a text input and a button {: #htmx-submitkey}

Start the server. Type a word and press Enter. Then type the same word and click Search.
Do both produce the same result?

[% inc submitkey.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is placing `hx-get` on the button rather than on the `<form>` element.
Clicking the button triggers HTMX and does a partial-page update. Pressing Enter in
the text field activates the form's native submit action (because no HTMX attribute
intercepts it), which sends a GET request to `/submit` and reloads the whole page.

Shows: where HTMX attributes belong when a form is involved, and how the browser's
native form submission can bypass HTMX.

To find it: press Enter in the input and observe whether the page reloads. If it does,
the form's native `action` attribute is firing. Move `hx-get`, `hx-target`, and
`hx-include` from the button to the `<form>` element so that both Enter and button-click
go through HTMX.

</details>

## Remove a record with a button click {: #htmx-getdelete}

Start the server and watch its terminal output while clicking Delete.
Which HTTP method does the server log for each request?

[% inc getdelete.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `hx-get` for an operation that deletes data. The HTTP specification
defines GET as safe and idempotent: it must not change server state, and anything that
caches or prefetches URLs (a browser, a CDN, a search engine crawler) may issue it
without the user's knowledge. Using GET for deletion means a prefetcher could
silently delete records.

Shows: HTTP method semantics — GET for reading, DELETE (or POST) for removing — and why
HTMX provides `hx-delete`, `hx-post`, and `hx-patch` as distinct attributes.

To find it: check the server log after clicking Delete. If it shows `GET` instead of
`DELETE`, the wrong attribute is being used. Replace `hx-get="/api/delete?id=1"` with
`hx-delete="/api/items/1"` and update the server to handle the `DELETE` method.

</details>

## Send additional parameters with a request {: #htmx-valsjson}

Start the server, click Subscribe, and read the server output.
Does the server report receiving a `plan` field?

[% inc valsjson.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using single quotes inside `hx-vals`. The `hx-vals` attribute must contain
valid JSON, and JSON requires double quotes for both keys and string values. HTMX
calls `JSON.parse` on the attribute value; when that fails it discards the extra fields
and sends the request without them. No error appears in the page.

Shows: JSON syntax (double quotes only) and how to use `hx-vals` to attach literal
values to a request.

To find it: open the browser console and look for a JSON parse error after clicking.
Change the attribute to use double quotes and single-quote the outer HTML attribute:
`hx-vals='{"plan": "premium", "version": 2}'`.

</details>

## Update two page areas from a single request {: #htmx-oob}

Start the server, click the button, and watch the notification area at the bottom.
Does it update?

[% inc oob.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is an ID mismatch between the server's out-of-band fragment and the element
on the page. The server returns `<div id="notification" hx-swap-oob="true">`, but
the page has `<div id="notifications">` (plural). HTMX looks for an element whose
`id` matches exactly, finds none, and silently discards the OOB fragment.

Shows: how out-of-band swaps work (`hx-swap-oob` targets an existing page element by
`id`) and why typos in IDs fail without any visible error.

To find it: search the server response in DevTools' Network tab for the OOB fragment.
Compare its `id` attribute to the `id` on the element you expect to update. Fix
whichever is wrong so the two match.

</details>

## Keep the URL bar in sync with displayed content {: #htmx-pushurl}

Start the server, click View Items, then reload the page.
What does the browser display after the reload?

[% inc pushurl.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `hx-push-url="true"` on a request that targets an API endpoint. After the
click the URL bar shows `/api/items`. Reloading the page sends a fresh GET request to
`/api/items`, which returns a bare `<ul>` fragment — no `<html>`, `<head>`, or `<body>`.
The browser displays raw HTML tags or a blank page.

Shows: what `hx-push-url` does (it changes the browser's URL history entry) and why the
pushed URL must correspond to a real page that returns a full HTML document.

To find it: after clicking, copy the URL from the address bar and paste it into a new
tab. If you see a fragment instead of a page, the URL should not have been pushed.
Use `hx-push-url="/items"` where `/items` returns a complete page, or remove
`hx-push-url` entirely if history support is not needed.

</details>

## Add HTMX to a page with existing links {: #htmx-boost}

Start the server, open `http://localhost:8000/boost`, and click "Download CSV".
Does the file download, or does something else happen?

[% inc boost.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `hx-boost="true"` on a `<nav>` that contains a download link. `hx-boost`
converts every link click in the container into an HTMX `GET` request that swaps the
response body into the current page. When the download link is clicked, HTMX fetches
`/download` via XHR. The browser's built-in download behavior only triggers during
direct navigation, not XHR, so `Content-Disposition: attachment` is ignored and the
raw CSV text is swapped into the page instead of saved as a file.

Shows: what `hx-boost` does to link clicks and that some links must remain as plain
navigation to work correctly.

To find it: add `hx-boost="false"` to the download link itself, which opts that
element out of the boosted container. HTMX respects this override and lets the browser
handle the click normally.

</details>

## Search using fields from a form {: #htmx-include}

Start the server, type a category, click Search, and read the server output.
Which fields did the server receive?

[% inc include.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `hx-include="input"`, which is a CSS selector matching every `<input>`
element on the entire page. The hidden `admin_token` field in the second form is
included and sent to the server alongside `category`, even though it belongs to a
completely different form that should never be submitted here.

Shows: how `hx-include` selectors work and why an overly broad selector can leak
data you did not intend to send.

To find it: look at the server log. If it shows fields you did not expect, the
selector is too broad. Replace `hx-include="input"` with
`hx-include="#search-form input"` (or `hx-include="closest form"` if the button
is inside the form) to include only the intended fields.

</details>

## Refresh a list when a new item is added {: #htmx-hxtrigger}

Start the server, add several items using the form, and watch the list below the form.
Does it update after each addition?

[% inc hxtrigger.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is on the server side. The `<ul>` listens for an `itemAdded` event dispatched
from the body (`hx-trigger="load, itemAdded from:body"`). HTMX fires that event when
it receives a response that includes the header `HX-Trigger: itemAdded`. The server's
`POST /api/add-item` handler does not send that header, so the event never fires and
the list only loads once (on page load) and never again.

Shows: the `HX-Trigger` response header as a server-to-client signaling mechanism,
and how HTMX can coordinate multiple page elements without JavaScript.

To find it: inspect the response headers for `POST /api/add-item` in DevTools' Network
tab. If `HX-Trigger` is absent, the server is not sending the signal. Add the header
to the response:

```python
self.send_header("HX-Trigger", "itemAdded")
```

The list will then re-fetch itself automatically after every successful addition.

</details>
