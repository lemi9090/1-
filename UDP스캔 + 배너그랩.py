import socket
import os
import struct
import time

# UDP 패킷 생성 함수
def create_udp_packet(target_ip, port, timeout=1):
    # UDP 헤더 생성
    header = struct.pack("HHHH", os.getpid() & 0xFFFF, 0, port, port)   
    header += struct.pack("!I", timeout)
    # 데이터 부분 생성
    data = b""
    # 패킷 생성
    packet = header + data
    return packet

# UDP 패킷 전송 함수
def send_udp_packet(target_ip, port, timeout=1):
    try:
        # raw socket 생성
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        raise

    # UDP 패킷 전송
    print(f"UDP 패킷 전송: IP {target_ip}, 포트 {port}")
    my_socket.sendto(create_udp_packet(target_ip, port, timeout), (target_ip, port))

    # 타임아웃 설정
    my_socket.settimeout(timeout)

    # 응답 수신
    try:
        response = my_socket.recv(1024)
        print(f"응답 수신: {response}")
    except socket.timeout:
        # 응답이 없으면 포트가 열려 있는 것으로 판단
        print(f"포트 {port} 응답 없음")
        return True
    except ConnectionResetError:
        # 원격 호스트가 연결을 끊었을 경우, 포트가 닫혀 있는 것으로 판단
        print(f"포트 {port} 연결 끊김")
        return False
    else:
        # 응답이 있으면 포트가 닫혀 있는 것으로 판단
        print(f"포트 {port} 응답 있음")
        return False

# UDP 스캔 함수
def udp_scan(target_ip):
    # 타겟 호스트 대신 IP 주소를 직접 입력받도록 수정
    open_udp_ports = []
    for port in range(0, 65536): 
        print(f"포트 {port} 스캔 시작")
        # 둘다 보내서 둘다 포트가 열려있다라고 나오는 경우만 open_udp_port 배열에 추가
        try:
            if send_udp_packet(target_ip, port) and send_udp_packet(target_ip, port, timeout=5):
                open_udp_ports.append(port)
        except Exception as e:
            continue
    return open_udp_ports
        

## UDP SERVICE  1 ##
def check_NTP(ip,port):
    print(f"{port} : checking NTP...")
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # NTP PROBE 생성
    pack = b"\xe3\x00\x04\xfa\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    pack2 = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    pack3 = b"\x00\x00\x00\x00\x00\x00\x00\x00\xc5\x4f\x23\x4b\x71\xb1\x52\xf3"
    pack = pack+pack2+pack3
    try:
        s.sendto(pack,(ip,port))
        s.settimeout(5)
        recv, server = s.recvfrom(1024)
        if recv is not None:
            return True
        return False
    except:
        return False
    finally:
        s.close()

## UDP SERVICE  2 ##
def check_DNS(ip, port):
    print(f"{port} : checking DNS...")
    message = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message,(ip, port))
        sock.settimeout(3)
        data, _ = sock.recvfrom(512)
        return True
    except Exception as e:
        return False
    finally:
        sock.close()

## UDP SERVICE  3 ##
def check_SIP(ip, port):
    print(f"{port} : checking SIP...")
    try:
        sip_options_msg = \
        'OPTIONS sip:{} SIP/2.0\r\n' \
        'Via: SIP/2.0/UDP {}:5060;branch=z9hG4bK-524287-1---0000000000000000\r\n' \
        'Max-Forwards: 70\r\n' \
        'Contact: <sip:{}>\r\n' \
        'To: <sip:{}>\r\n' \
        'From: anonymous<sip:anonymous@anonymous.invalid>;tag=0000000000000000\r\n' \
        'Call-ID: 00000000000000000000000000000000@anonymous.invalid\r\n' \
        'CSeq: 1 OPTIONS\r\n' \
        'Accept: application/sdp\r\n' \
        'Content-Length: 0\r\n\r\n'.format(ip, ip, ip, ip)
        # UDP 소켓 생성 및 SIP 서버로 메시지 전송
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(sip_options_msg.encode(), (ip, port)) 
        sock.settimeout(3)
        data, addr = sock.recvfrom(4096) #최대로 받을 양 4096 바이트(버퍼크기)
        return True
        
    except Exception as e:
        return False
    finally:
        sock.close() #리소스 해제

def udpBannergrab(ip, port):
    service = None
    try:
        if (check_NTP(ip, port)):
            service = "ntp"
        elif (check_DNS(ip, port)):
            service = "dns"
        elif (check_SIP(ip, port)):
            service = "sip"

        if service is not None:
            print(f"{ip} : {port} : {service}")
            return service
    except Exception as e:
            return "대상 컴퓨터에서 연결을 거부"


def main():
    target_ip = input("대상 IP 주소를 입력하세요: ")
    open_udp_ports = udp_scan(target_ip)
    services = []
    for port in open_udp_ports:
        service = udpBannergrab(target_ip, port)
        services.append({'port': port, 'service': service})
    print (services)

main()

