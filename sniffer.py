from scapy.all import sniff, DNSQR


def extract_domain(packet):
    if packet.haslayer(DNSQR):
        domain = packet[DNSQR].qname.decode("utf-8").rstrip('.')
        return domain
    return None


def start_sniffing(callback):
    print("Sniff started. Press Ctrl+C to stop.")
    sniff(filter="udp port 53", prn=callback, store=0)
