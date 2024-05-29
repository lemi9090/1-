from scapy.layers.inet import ICMP, IP, TCP, sr1
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def icmp_probe(ip):
    icmp_packet = IP(dst=ip) / ICMP()
    resp_packet = sr1(icmp_packet, timeout=10)
    return resp_packet is not None

def scan_port(ip, port, open_tcp_ports):
    syn_packet = IP(dst=ip) / TCP(dport=port, flags='S')
    resp_packet = sr1(syn_packet, timeout=10)
    if resp_packet is not None:
        if resp_packet.haslayer(TCP) and (resp_packet[TCP].flags & 0x12 == 0x12):
            open_tcp_ports.append(port)
            print(f'{ip}:{port} is open/{resp_packet.sport}')
        else:
            print(f'{ip}:{port} is closed')
    else:
        print(f'{ip}:{port} is filtered or no response')

def syn_scan(ip, start_port, end_port):
    open_tcp_ports = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:   #실행 속도 증가
        futures = []
        for port in range(start_port, end_port + 1):
            futures.append(executor.submit(scan_port, ip, port, open_tcp_ports))
        
        for future in futures:
            future.result()  

    return open_tcp_ports

def scan(ip):
    ip = socket.gethostbyname(ip)
    start_port = 0
    end_port = 65535

    try:
        if icmp_probe(ip):
            open_ports = syn_scan(ip, start_port, end_port)
            print('Syn Scan completed!')
            return open_ports
        else:
            print('Failed to send ICMP packet')
            return False
    except Exception as e:
        print('Error:', e)
        return False

