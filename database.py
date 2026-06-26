import sqlite3
from datetime import datetime


class DNSDatabase:
    def __init__(self, db_name="dns_logs.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS requests 
                          (id INTEGER PRIMARY KEY, timestamp DATETIME, domain TEXT)''')
        self.conn.commit()

    def log_query(self, domain):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.conn.execute(
            "INSERT INTO requests (timestamp, domain) VALUES (?, ?)", (timestamp, domain))
        self.conn.commit()
        print(f"[{timestamp}] Logged: {domain}")
