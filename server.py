"""
DNS Logger – local server
=========================
Serves dashboard.html and exposes /data as JSON from dns_logs.db.

Usage:
    python server.py                      # uses dns_logs.db in same folder
    python server.py /path/to/dns_logs.db # custom path
    python server.py --port 8080          # custom port (default: 5050)

Then open: http://localhost:5050
"""

import json
import sqlite3
import sys
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# ── Config ─────────────────────────────────────────────────────────────────
DEFAULT_DB   = "dns_logs.db"
DEFAULT_PORT = 5050
SCRIPT_DIR   = Path(__file__).parent


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("db", nargs="?", default=DEFAULT_DB, help="Path to SQLite DB")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    return p.parse_args()


def query_db(db_path: str, limit: int = 2000) -> list[dict]:
    """Return rows from requests table as a list of dicts."""
    path = Path(db_path)
    if not path.exists():
        return []
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT id, timestamp, domain FROM requests ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cur.fetchall()]


# ── HTTP handler ────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    db_path: str = DEFAULT_DB  # set by main()

    def log_message(self, fmt, *args):
        # Quiet server log — only print errors
        if args and str(args[1]) not in ("200", "304"):
            super().log_message(fmt, *args)

    def send_json(self, payload: object, status: int = 200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, file_path: Path, mime: str):
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/") or "/"

        # /data  →  JSON from SQLite
        if path == "/data":
            qs    = parse_qs(parsed.query)
            limit = int(qs.get("limit", [2000])[0])
            rows  = query_db(self.db_path, limit)
            self.send_json({"rows": rows, "total": len(rows)})

        # /  or  /dashboard.html  →  serve the HTML file
        elif path in ("/", "/dashboard.html"):
            html = SCRIPT_DIR / "dashboard.html"
            if html.exists():
                self.send_file(html, "text/html; charset=utf-8")
            else:
                self.send_json({"error": "dashboard.html not found"}, 404)

        else:
            self.send_json({"error": "not found"}, 404)


def main():
    args = get_args()
    Handler.db_path = args.db

    db_exists = Path(args.db).exists()
    print(f"\n  DNS Logger Dashboard")
    print(f"  ────────────────────────────────")
    print(f"  DB   : {Path(args.db).resolve()} {'✓' if db_exists else '⚠ (not found yet)'}")
    print(f"  URL  : http://localhost:{args.port}")
    print(f"  Stop : Ctrl+C\n")

    server = HTTPServer(("", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
