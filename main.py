from sniffer import start_sniffing, extract_domain
from database import DNSDatabase
import sys


def main():
    db = DNSDatabase()

    def packet_callback(packet):
        domain = extract_domain(packet)
        if domain:
            db.log_query(domain)

    try:
        start_sniffing(packet_callback)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    main()
