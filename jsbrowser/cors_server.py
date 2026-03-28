"""Simple API server that is missing the CORS header.

Run with:  python cors_server.py
Then open cors.html in a browser and click "Fetch".
The browser will refuse the response with a CORS error;
the same request works fine from curl or Python.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            body = json.dumps({"items": ["alpha", "beta", "gamma"]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            # BUG: missing Access-Control-Allow-Origin header;
            #      browsers block the response; curl and Python requests do not
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Serving on http://localhost:8000  (Ctrl-C to stop)")
    server.serve_forever()
