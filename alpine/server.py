"""Single server for all Alpine.js bug examples.

Run with:  uv run server.py
Then open http://localhost:8000 in a browser.

Each example is available at http://localhost:8000/<slug>.  The slugs are:
  wrongscope  noprevent   xcloak      stringdata  xiftemplate modelbind
  nexttick    asyncinit   storeorder  forkey      globalstate keyboardtarget
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))

SLUGS = (
    "wrongscope",
    "noprevent",
    "xcloak",
    "stringdata",
    "xiftemplate",
    "modelbind",
    "nexttick",
    "asyncinit",
    "storeorder",
    "forkey",
    "globalstate",
    "keyboardtarget",
)

TITLES = {
    "wrongscope": "x-data on child element, directives on parent see nothing",
    "noprevent": "@submit without .prevent causes a full page reload",
    "xcloak": "Missing [x-cloak] CSS lets content flash before init",
    "stringdata": "x-data with a string literal instead of an object",
    "xiftemplate": "x-if on a <div> instead of a <template>",
    "modelbind": "x-bind:value without @input is one-way only",
    "nexttick": "focus() called before x-show makes the element visible",
    "asyncinit": "named function updates global scope instead of Alpine state",
    "storeorder": "Alpine.store read before it is registered",
    "forkey": "x-for without :key reuses wrong DOM nodes on deletion",
    "globalstate": "external object mutation bypasses Alpine's reactive proxy",
    "keyboardtarget": "@keydown on an unfocusable element never fires",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]

        if path in ("/", ""):
            self._serve_index()
        elif path.lstrip("/") in SLUGS:
            self._serve_file(path.lstrip("/") + ".html")
        elif path == "/api/greeting":
            body = json.dumps({"message": "Hello from the server!"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._html("<p>Not found.</p>", 404)

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
        self._html(f"<html><body><h1>Alpine.js Examples</h1><ul>{links}</ul></body></html>")

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Serving on http://localhost:8000  (Ctrl-C to stop)")
    server.serve_forever()
