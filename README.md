# DNS Logger 🔍

A lightweight, modular network utility designed to capture DNS queries on your home network and persist them to a local SQLite database. Includes a real-time web dashboard for visualization and analysis.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Starting the Packet Sniffer](#starting-the-packet-sniffer)
  - [Running the Dashboard Server](#running-the-dashboard-server)
  - [Exporting Data](#exporting-data)
- [API Reference](#api-reference)
- [Dashboard](#dashboard)
- [Technical Details](#technical-details)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## 📖 Overview

**DNS Logger** is a passive network monitoring tool that acts as an invisible observer on your home network. By intercepting UDP traffic on port 53, it extracts domain names from DNS queries in real-time and stores them in a local SQLite database. The included web dashboard provides a user-friendly interface to visualize DNS traffic patterns, identify top domains, and audit network activity.

**Use Cases:**
- Monitor what devices on your network are accessing
- Identify unexpected or suspicious domain queries
- Audit network traffic for security purposes
- Analyze DNS query patterns over time
- Educational tool for learning about network protocols

---

## ✨ Features

- 🌐 **Real-Time DNS Capture**: Intercepts and logs DNS queries as they happen
- 💾 **SQLite Persistence**: All queries stored in a local database with timestamps
- 📊 **Interactive Dashboard**: 
  - Hourly query volume chart
  - Top 10 most-queried domains
  - Live query log with full details
  - Date range filtering
  - Domain search functionality
- 🚀 **Lightweight**: Minimal dependencies (only `scapy`)
- 🔧 **Modular Design**: Well-separated concerns (sniffer, database, server, export)
- 📤 **JSON Export**: Export captured data for offline analysis
- 🎨 **Modern UI**: Dark-themed, responsive web interface

---

## 🔧 How It Works

The DNS Logger operates in two phases:

### **Phase 1: Packet Sniffing** (main.py)
1. **Initialization**: Creates a SQLite database (`dns_logs.db`) if it doesn't exist
2. **Packet Capture**: Uses `scapy` to sniff all packets on your network interface
3. **DNS Filtering**: Filters for UDP traffic on port 53 (DNS protocol)
4. **Domain Extraction**: Parses the DNS Query Record (DNSQR) layer to extract the requested domain
5. **Logging**: Stores domain name and timestamp in the database

### **Phase 2: Web Dashboard** (server.py)
1. **HTTP Server**: Starts a simple HTTP server on port 5050
2. **Dashboard Serving**: Serves the interactive HTML dashboard
3. **Data API**: Exposes `/data` endpoint returning JSON from the database
4. **Real-Time Updates**: Dashboard auto-refreshes every 30 seconds

**Architecture Flow:**
```
Network Traffic
    ↓
[scapy] Packet Capture
    ↓
UDP Port 53 Filter
    ↓
DNS Query Parser
    ↓
SQLite Database (dns_logs.db)
    ↓
HTTP Server (/data endpoint)
    ↓
Web Dashboard (HTML + JavaScript)
```

---

## 📁 Project Structure

```
dns-logger/
├── main.py              # Entry point for packet sniffing
├── server.py            # HTTP server for dashboard
├── sniffer.py           # DNS packet sniffing logic
├── database.py          # SQLite database management
├── dashboard.html       # Web dashboard UI
├── export_json.py       # Data export utility
├── requirements.txt     # Python dependencies
├── dns_logs.db          # SQLite database (auto-created)
├── README.md            # This file
├── LICENSE              # MIT License
└── dns_data.json        # Exported data (optional)
```

### **File Descriptions**

| File | Purpose |
|------|---------|
| `main.py` | Main entry point that starts the DNS sniffer |
| `server.py` | HTTP server serving dashboard and data API |
| `sniffer.py` | Core sniffing logic using scapy |
| `database.py` | SQLite wrapper for log persistence |
| `dashboard.html` | Full-featured web UI with charts |
| `export_json.py` | Utility to export database to JSON |

---

## 📋 Prerequisites

- **Python 3.7+**
- **Root/Administrator privileges** (required for raw network packet capture)
- **Linux/macOS/Windows** (any OS with Python and raw socket support)

### **System Requirements**

- Scapy (installed via pip)
- SQLite3 (included with Python)
- Web browser to view dashboard

---

## 🚀 Installation

### **Clone the Repository**

```bash
git clone https://github.com/yourusername/dns-logger.git
cd dns-logger
```

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**
```
scapy
```

### **Verify Installation**

```bash
python3 -c "import scapy; print('Scapy installed successfully')"
```

---

## 📖 Usage

The DNS Logger has two main components that can run independently:

### **Starting the Packet Sniffer**

To start capturing DNS queries, run:

```bash
sudo python3 main.py
```

**Important Notes:**
- ⚠️ **Root privileges required** (`sudo`) for raw socket access
- Press `Ctrl+C` to stop sniffing gracefully
- Queries are logged to `dns_logs.db` in real-time
- Console output shows each captured domain with timestamp

**Example Output:**
```
Sniff started. Press Ctrl+C to stop.
[2026-06-27 14:23:45] Logged: github.com
[2026-06-27 14:23:46] Logged: www.google.com
[2026-06-27 14:23:47] Logged: api.github.com
...
```

### **Running the Dashboard Server**

In a **separate terminal**, start the web dashboard:

```bash
python3 server.py
```

**Optional Arguments:**

```bash
# Use custom port
python3 server.py --port 8080

# Use custom database path
python3 server.py /path/to/dns_logs.db

# Combine both
python3 server.py /path/to/dns_logs.db --port 8080
```

**Default Configuration:**
- **Database**: `dns_logs.db` (in current directory)
- **Port**: `5050`
- **URL**: `http://localhost:5050`

Once running, open your browser to the displayed URL to view the dashboard.

### **Exporting Data**

Export captured data to JSON format for offline analysis or integration with other tools:

```bash
python3 export_json.py
```

**Optional Arguments:**

```bash
# Export from specific database
python3 export_json.py /path/to/dns_logs.db

# Export to custom file
python3 export_json.py --out /path/to/output.json

# Both options
python3 export_json.py /path/to/dns_logs.db --out /path/to/custom.json
```

**Output Example:**
```json
{
  "exported_at": "2026-06-27T14:30:00",
  "total": 126,
  "rows": [
    {
      "id": 126,
      "timestamp": "2026-06-27 14:30:00",
      "domain": "github.com"
    },
    ...
  ]
}
```

#### **Using Exported JSON with Dashboard**

To view the dashboard offline using exported data:

1. Export the data: `python3 export_json.py`
2. Edit `dashboard.html` and change line 8:
   ```javascript
   // OLD:
   const DATA_URL = "/data";
   
   // NEW:
   const DATA_URL = "./dns_data.json";
   ```
3. Open `dashboard.html` directly in your browser (no server needed)

---

## 🔌 API Reference

### **GET /data**

Returns all logged DNS queries from the database.

**Endpoint:** `http://localhost:5050/data`

**Parameters:**
- `limit` (optional, default: 2000): Maximum number of records to return

**Example Requests:**

```bash
# Get all queries (up to 2000)
curl http://localhost:5050/data

# Get last 100 queries
curl "http://localhost:5050/data?limit=100"
```

**Response Format:**

```json
{
  "rows": [
    {
      "id": 1,
      "timestamp": "2026-06-27 14:23:45",
      "domain": "github.com"
    },
    {
      "id": 2,
      "timestamp": "2026-06-27 14:23:46",
      "domain": "www.google.com"
    }
  ],
  "total": 2
}
```

### **GET /**

Serves the dashboard HTML file.

**Endpoint:** `http://localhost:5050/`

**Response:** HTML dashboard page with embedded JavaScript and CSS

---

## 📊 Dashboard

The web dashboard provides a comprehensive view of your DNS traffic:

### **Components**

1. **Status Badge** - Shows connection status to data API (green = OK, red = error)

2. **Hourly Query Volume Chart**
   - Bar chart showing DNS queries per hour
   - Helps identify peak DNS activity times
   - Real-time updates every 30 seconds

3. **Top 10 Domains**
   - Lists most frequently queried domains
   - Shows query count for each domain
   - Useful for identifying commonly accessed services

4. **Live Query Log**
   - Complete list of all captured queries
   - Includes ID, timestamp, and domain name
   - Shows most recent queries first
   - Sortable and searchable

5. **Filters & Search**
   - **Date Range**: Filter queries by date
   - **Domain Search**: Find specific domains
   - **Auto-Refresh**: Updates every 30 seconds

### **Design**

- **Modern Dark Theme**: Easy on the eyes for extended monitoring
- **Responsive Layout**: Works on desktop and tablet
- **Performance Optimized**: Efficiently handles thousands of records
- **Real-Time Updates**: Live data refresh without page reload

---

## 🔬 Technical Details

### **Database Schema**

The SQLite database uses a single table:

```sql
CREATE TABLE requests (
  id        INTEGER PRIMARY KEY,
  timestamp DATETIME,
  domain    TEXT
)
```

**Schema Details:**
- `id`: Auto-incrementing primary key
- `timestamp`: Query timestamp in format `YYYY-MM-DD HH:MM:SS`
- `domain`: Requested domain name (e.g., `github.com`)

### **Packet Parsing**

The sniffer extracts domains from DNS packets:

```python
# DNS packet structure:
# Ethernet → IP → UDP → DNS
# The DNSQR (DNS Query Record) layer contains:
# - qname: The domain name being queried
# - qtype: Query type (A, AAAA, MX, etc.)
# - qclass: Query class (usually IN for Internet)
```

**Example**: When you visit `github.com`, the sniffer captures:
- Domain: `github.com`
- Timestamp: Current time
- Query type: `A` (IPv4 address lookup, typically)

### **Port 53 (DNS Protocol)**

DNS uses UDP protocol on port 53 for queries and responses:
- **Fast**: UDP is connectionless and has low overhead
- **Standard**: Port 53 is the IANA-assigned DNS port
- **Observable**: All DNS queries pass through port 53

---

## ⚙️ Configuration

### **Custom Network Interface**

To sniff on a specific network interface, edit `sniffer.py`:

```python
# Change this line:
sniff(filter="udp port 53", prn=callback, store=0)

# To (example with 'eth0'):
sniff(iface="eth0", filter="udp port 53", prn=callback, store=0)
```

### **Database Location**

By default, `dns_logs.db` is created in the current directory. To use a custom location:

```bash
# Edit database.py line 6:
# OLD: def __init__(self, db_name="dns_logs.db"):
# NEW: def __init__(self, db_name="/var/log/dns_logs.db"):
```

### **Server Port**

Change the port via command-line argument:

```bash
python3 server.py --port 8080
```

Or edit `server.py` line 21:

```python
DEFAULT_PORT = 8080  # Change from 5050
```

---

## 🐛 Troubleshooting

### **"Permission denied" error when running main.py**

**Problem**: Packet sniffing requires root privileges

**Solution**:
```bash
sudo python3 main.py
```

### **"No module named 'scapy'" error**

**Problem**: Scapy not installed

**Solution**:
```bash
pip install scapy
```

### **"Address already in use" when running server.py**

**Problem**: Port 5050 is already in use

**Solutions**:
- Kill the existing process: `lsof -i :5050 | grep python | awk '{print $2}' | xargs kill -9`
- Use a different port: `python3 server.py --port 8080`
- Wait a minute for the port to be released

### **No queries appearing in dashboard**

**Problem**: Sniffer not capturing queries

**Causes & Solutions**:
1. **Sniffer not running**: Start `main.py` in another terminal with `sudo`
2. **Database issue**: Check if `dns_logs.db` exists and is writable
3. **Wrong interface**: Specify the correct network interface in `sniffer.py`
4. **Firewall blocking**: Ensure raw socket access is allowed

### **Dashboard shows "Error loading data"**

**Problem**: `/data` API endpoint failing

**Solutions**:
1. Verify server is running: `curl http://localhost:5050/data`
2. Check database permissions: `ls -la dns_logs.db`
3. Check server logs for errors (if verbose mode is enabled)

### **Very slow dashboard with thousands of records**

**Problem**: Large dataset impacts performance

**Solutions**:
1. Limit API response: `curl "http://localhost:5050/data?limit=500"`
2. Archive old data to separate database
3. Clear old records: Delete from `requests` table with a date filter

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** your changes: `git commit -m 'Add your feature'`
4. **Push** to the branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

### **Potential Enhancements**

- GeoIP location of DNS servers
- Domain categorization (malware, ads, etc.)
- Query type analysis (A, AAAA, CNAME, etc.)
- Multi-interface support
- Docker containerization
- Database compression and archival
- Email alerts for suspicious domains
- Advanced filtering and pattern detection

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ⚠️ Disclaimer

**IMPORTANT**: This tool is intended for **educational and authorized network monitoring purposes only**.

### **Legal Compliance**

- **Network Authorization**: Only monitor networks you own or have explicit written permission to monitor
- **Privacy Laws**: Comply with all applicable local, state, and federal laws regarding network monitoring
- **Ethical Use**: Do not use this tool for unauthorized surveillance or malicious purposes
- **Third-Party Rights**: Respect the privacy and rights of all network users

### **Liability**

The authors and contributors of DNS Logger are **not responsible** for:
- Unauthorized use of this tool
- Legal violations resulting from its use
- Damages caused by improper operation
- Privacy breaches or data leaks

**By using this tool, you agree to use it responsibly and legally.**

---

## 📞 Support & Questions

For issues, questions, or suggestions:

1. **Check the [Troubleshooting](#troubleshooting) section**
2. **Open an Issue** on GitHub
3. **Submit a Pull Request** with fixes or improvements

---

## 🎓 Learning Resources

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [DNS Protocol Overview](https://en.wikipedia.org/wiki/Domain_Name_System)
- [Python SQLite Tutorial](https://docs.python.org/3/library/sqlite3.html)
- [HTTP Server in Python](https://docs.python.org/3/library/http.server.html)

---

**Happy monitoring! 🔍**

In
