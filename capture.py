from scapy.all import sniff, IP, TCP
import sqlite3
from datetime import datetime

# Setup database (our "evidence locker")
conn = sqlite3.connect('traffic.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS alerts
                (id INTEGER PRIMARY KEY, 
                 time TEXT, 
                 message TEXT)''')

def log_alert(message):
    """Save alerts to database"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO alerts (time, message) VALUES (?, ?)", (now, message))
    conn.commit()
    print(f" ALERT: {message}")

def analyze_packet(packet):
    """Detect hacker activity"""
    if packet.haslayer(TCP) and packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        
        # Detection 1: Port scans (like a thief checking doors)
        if dst_port > 10000:  
            log_alert(f"Suspicious port scan from {src_ip} on port {dst_port}")
        
        # Detection 2: SSH brute-force (like guessing a lock combination)
        if dst_port == 22 and packet[TCP].flags == 'R':  # SSH port + reset flag
            log_alert(f" Bruteforce attempt from {src_ip}")

# Start surveillance!
print(" Sniffing network traffic... Press CTRL+C to stop")
sniff(prn=analyze_packet, filter="tcp", store=0)
