from portscan import udpscan, synscan
from servicescan import servicescan

print("1.(TCP_SYN SCAN) 2.(UDP SCAN)")
while True:  
    num = input(">>")
    if num == "1" or num == "2":
        break
    else:
        print("please type 1(syn) or 2(udp)")


ip = input("IP : ")

while True:
    if num == "1": # TCP_SYN 스캔
        tcp_ports = synscan.scan(ip)
        print(tcp_ports)
        tcp_services = servicescan.ServiceScan(ip,tcp_ports,'tcp')
        
        for tcp_service in tcp_services:
            print(f"PORT : {tcp_service[0]} SERVICE : {tcp_service[1]}")
        break
    if num == "2" : # UDP 스캔
        udp_ports = udpscan.udp_scan(ip)
        print(udp_ports)
        udp_services = servicescan.ServiceScan(ip,udp_ports,'udp')
        for udp_service in udp_services:
            print(f"PORT : {udp_service[0]} SERVICE : {udp_service[1]}")
        break