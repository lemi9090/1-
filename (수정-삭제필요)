import socket
import requests

def check_http(ip, port):
    try:
        response = requests.get(f"http://{ip}:{port}", timeout=3)
        return True, f"HTTP {response.status_code}"
    except requests.RequestException:
        return False, "Not HTTP"

def grab_banner(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=3) as s:
            banner = s.recv(1024).decode(errors='ignore')
            return True, banner
    except socket.error:
        return False, "Connection refused or timed out"

def read_tested_ports(file_path):
    with open(file_path, 'r') as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]


def main():
    ip = "127.0.0.1"
    file_path = "C:/Users/ADMIN/Desktop/실습/스캐닝, 소캣 프로그래밍/open_ports.txt"
    open_ports = read_tested_ports(file_path)  
    print(f"Open ports: {open_ports}")
    
    for port in open_ports:
        is_http, http_result = check_http(ip, port)
        if is_http:
            print(f"Port {port}: {http_result}")
        else:
            is_service, banner_result = grab_banner(ip, port)
            if is_service:
                print(f"Port {port}: {banner_result}")
            else:
                print(f"Port {port}: {banner_result}")

if __name__ == "__main__":
    main()
