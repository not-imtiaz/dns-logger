"""
export_json.py — Option A (static / offline mode)
===================================================
Exports dns_logs.db → dns_data.json so you can open dashboard.html
directly in a browser without running server.py.

After exporting, edit the top of dashboard.html and change:
    const DATA_URL = "/data";
to:
    const DATA_URL = "./dns_data.json";

Usage:
    python export_json.py
    python export_json.py /path/to/dns_logs.db
    python export_json.py --out /path/to/output.json
"""

import argparse
import json
import sqlite3
from pathlib import Path
from datetime import datetime


def export(db_path: str, out_path: str) -> None:
    db = Path(db_path)
    if not db.exists():
        print(f"✗ Database not found: {db.resolve()}")
        return

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        rows = [
            dict(row)
            for row in conn.execute(
                "SELECT id, timestamp, domain FROM requests ORDER BY timestamp DESC"
            )
        ]

    payload = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "total": len(rows),
        "rows": rows,
    }
    Path(out_path).write_text(json.dumps(payload, indent=2))
    print(f"✓ Exported {len(rows):,} rows → {Path(out_path).resolve()}")
    print(f"  Now open dashboard.html in your browser.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("db",    nargs="?", default="dns_logs.db")
    p.add_argument("--out", default="dns_data.json")
    args = p.parse_args()
    export(args.db, args.out)
