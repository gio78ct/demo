import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from offers.csv_import import parse_csv
from offers.sources import SOURCES

STATIC = os.path.join(os.path.dirname(__file__), "static")


def search(params):
    q = params.get("q", [""])[0]
    wanted = params.get("source", [""])[0].split(",") if params.get("source") else list(SOURCES)
    offers, errors = [], {}
    for name in wanted:
        src = SOURCES.get(name)
        if not src:
            continue
        if not src.available():
            errors[name] = "non configurata (credenziali mancanti)"
            continue
        try:
            offers += [o.to_dict() for o in src.search(q)]
        except Exception as e:  # una fonte che fallisce non blocca le altre
            errors[name] = str(e)
    return {"offers": offers, "errors": errors}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/search":
            body, ctype = json.dumps(search(parse_qs(url.query))).encode(), "application/json"
        elif url.path == "/api/sources":
            body = json.dumps({n: s.available() for n, s in SOURCES.items()}).encode()
            ctype = "application/json"
        elif url.path in ("/", "/index.html"):
            with open(os.path.join(STATIC, "index.html"), "rb") as f:
                body, ctype = f.read(), "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != "/api/import":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        if length > 2_000_000:
            self.send_error(413)
            return
        status, payload = import_csv(self.rfile.read(length))
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def import_csv(raw):
    try:
        offers = parse_csv(raw.decode("utf-8-sig"), default_source="importato")
    except (ValueError, UnicodeDecodeError) as e:
        return 400, {"error": str(e)}
    return 200, {"offers": [o.to_dict() for o in offers]}


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"http://localhost:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
