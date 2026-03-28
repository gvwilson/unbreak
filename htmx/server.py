"""Single server for all HTMX bug examples.

Run with:  uv run server.py
Then open http://localhost:8000 in a browser.

Each example is available at http://localhost:8000/<slug>.  The slugs are:
  wrongswap   notarget   indicator   trigger    submitkey
  getdelete   valsjson   oob         pushurl    boost
  include     hxtrigger
"""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))

# Delay in seconds for the /api/slow endpoint (indicator example).
SLOW_DELAY = 2

# In-memory list for the hxtrigger example, pre-populated with two items.
ITEMS = ["Apple", "Banana"]

SLUGS = (
    "wrongswap",
    "notarget",
    "indicator",
    "trigger",
    "submitkey",
    "getdelete",
    "valsjson",
    "oob",
    "pushurl",
    "boost",
    "include",
    "hxtrigger",
)

TITLES = {
    "wrongswap": "outerHTML swap removes the target element",
    "notarget": "Response replaces the triggering element",
    "indicator": "Loading indicator never appears",
    "trigger": "Search fires on every keystroke",
    "submitkey": "Pressing Enter causes a full page reload",
    "getdelete": "GET used for a state-changing deletion",
    "valsjson": "Single-quoted JSON in hx-vals",
    "oob": "Out-of-band swap silently ignored",
    "pushurl": "Pushed URL returns a fragment on refresh",
    "boost": "hx-boost intercepts a download link",
    "include": "hx-include sends unintended form fields",
    "hxtrigger": "Missing HX-Trigger response header",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", ""):
            self._serve_index()
        elif path.lstrip("/") in SLUGS:
            self._serve_file(path.lstrip("/") + ".html")
        elif path == "/api/data":
            self._html("<p>Result: 42</p>")
        elif path == "/api/slow":
            time.sleep(SLOW_DELAY)
            self._html("<p>Data loaded after delay.</p>")
        elif path == "/api/suggest":
            qs = parse_qs(parsed.query)
            q = qs.get("q", [""])[0].lower()
            print(f"  /api/suggest called with q={q!r}")
            words = ["apple", "apricot", "avocado", "banana", "blueberry", "cherry", "date"]
            matches = [w for w in words if w.startswith(q)] if q else []
            if matches:
                items = "".join(f"<li>{w}</li>" for w in matches)
                self._html(f"<ul>{items}</ul>")
            else:
                self._html("<p>No matches.</p>")
        elif path == "/submit":
            qs = parse_qs(parsed.query)
            query = qs.get("query", ["(none)"])[0]
            self._html(
                "<html><body>"
                "<h1>Native form submission</h1>"
                f"<p>Received query: <code>{query}</code></p>"
                "<p>The page reloaded because the form's native GET action fired.</p>"
                "</body></html>"
            )
        elif path == "/api/results":
            qs = parse_qs(parsed.query)
            query = qs.get("query", [""])[0]
            self._html(f"<p>HTMX result for: <code>{query}</code></p>")
        elif path == "/api/delete":
            qs = parse_qs(parsed.query)
            item_id = qs.get("id", ["?"])[0]
            print(f"  WARNING: deletion requested via GET for id={item_id!r}")
            self._html(
                f"<p>Deleted item {item_id!r} "
                "(server state changed by a GET request).</p>"
            )
        elif path == "/api/items":
            # Returns a bare fragment, not a full HTML page (pushurl bug).
            self._html("<ul><li>Item A</li><li>Item B</li><li>Item C</li></ul>")
        elif path == "/items":
            self._html(
                "<html><body>"
                "<h1>Items</h1>"
                "<ul><li>Item A</li><li>Item B</li><li>Item C</li></ul>"
                "</body></html>"
            )
        elif path == "/download":
            csv = "name,score\nAlice,95\nBob,87\nCarol,91\n"
            body = csv.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", 'attachment; filename="data.csv"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/items-list":
            rows = "".join(f"<li>{item}</li>" for item in ITEMS)
            self._html(f"<ul>{rows}</ul>")
        else:
            self._html("<p>Not found.</p>", 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._body()

        if path == "/api/search":
            self._html(
                "<ul>"
                "<li>Result A</li>"
                "<li>Result B</li>"
                "<li>Result C</li>"
                "</ul>"
            )
        elif path == "/api/submit":
            print(f"  POST /api/submit received: {body!r}")
            self._html("<p>Submitted via HTMX.</p>")
        elif path == "/submit":
            print(f"  POST /submit (native form action) received: {body!r}")
            self._html(
                "<html><body>"
                "<h1>Native form submission</h1>"
                "<p>The page reloaded because the native POST action fired.</p>"
                "</body></html>"
            )
        elif path == "/api/vals":
            print(f"  POST /api/vals body: {body!r}")
            params = parse_qs(body)
            decoded = {k: v[0] for k, v in params.items()}
            self._html(f"<p>Server received: <code>{json.dumps(decoded)}</code></p>")
        elif path == "/api/action":
            # Returns main content plus an out-of-band swap targeting the WRONG id.
            # The page has id="notifications" but the OOB fragment uses id="notification".
            fragment = (
                "<p>Action completed.</p>"
                '<div id="notification" hx-swap-oob="true">'
                "<strong>1 new message</strong>"
                "</div>"
            )
            self._html(fragment)
        elif path == "/api/search-fields":
            print(f"  POST /api/search-fields body: {body!r}")
            params = parse_qs(body)
            decoded = {k: v[0] for k, v in params.items()}
            self._html(f"<p>Server received: <code>{json.dumps(decoded)}</code></p>")
        elif path == "/api/add-item":
            params = parse_qs(body)
            name = params.get("name", ["Unnamed"])[0]
            ITEMS.append(name)
            print(f"  Added item: {name!r}  (list now has {len(ITEMS)} items)")
            # BUG: the HX-Trigger header is not sent here;
            # BUG: the "itemAdded" event never fires and the list never refreshes
            self._html(f"<p>Added {name!r}. (List will not refresh automatically.)</p>")
        else:
            self._html("<p>Not found.</p>", 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/items/"):
            item_id = path.split("/")[-1]
            print(f"  DELETE /api/items/{item_id} — correct HTTP verb used")
            self._html(f"<p>Deleted item {item_id!r} via DELETE.</p>")
        else:
            self._html("<p>Not found.</p>", 404)

    # ------------------------------------------------------------------

    def _body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode() if length else ""

    def _html(self, html, status=200):
        body = html.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, filename):
        filepath = os.path.join(HERE, filename)
        try:
            with open(filepath, "rb") as fh:
                body = fh.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self._html("<p>File not found.</p>", 404)

    def _serve_index(self):
        links = "".join(
            f'<li><a href="/{slug}">{TITLES[slug]}</a></li>' for slug in SLUGS
        )
        self._html(f"<html><body><h1>HTMX Examples</h1><ul>{links}</ul></body></html>")

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Serving on http://localhost:8000  (Ctrl-C to stop)")
    server.serve_forever()
