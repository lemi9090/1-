import socket
import sys
import time
import random
# import threading # ThreadPoolExecutor 함수를 사용하므로 굳이 import 시켜 사용할 필요 없음
import concurrent.futures # 멀티쓰레드 

target_host ='127.0.0.1'
start_port = 1
end_port = 3308

def scan_port (host,port):  # 현재 포트의 값이 출력되어 나온다.
    try : 
        time.sleep(0.5)
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
 
        result = sock.connect_ex((host, port))
        if result == 0: 
            return port
    except socket.gaierror:
        return "Hostname is not resolved"
    except socket.error:
        return "Could'nt connect to server"
       
def main():
    target_ip = socket.gethostbyname(target_host)
    numbers = list(range(start_port, end_port +1))
    random.shuffle(numbers)
    num_threads = 10
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor :
        futures = [executor.submit(scan_port,target_ip, number) for number in numbers] # scan_port는 port 값만 출력한다. taget_ip를 넣어서 host 정보도 넣어 줘야 한다.
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            try:
                if result:
                    open_ports.append(result)
                    print(f'Port {result} is open')
            except Exception as e : # 예외들을 모으기 위해 e라는 객체를 새로 만들었다. 
                print(f'error occured : {e}') 
    if open_ports :
        with open('open_ports.txt', 'w') as f:
            for port in open_ports:
                f.write(f'{port}\n')
        print('Open ports have been saved to open_ports.txt')
    else:
        print('No open ports found')

    
if __name__=='__main__':
    main()
# print 함수는 정보나 결과를 사용자에게 바로 표시하려는 경우에 사용
# return 함수는 함수에서 값을 반환하려는 경우에 사용
#만약 scan_port 함수에서 직접 결과를 출력하도록 만들고 싶다면, 
# return 대신 print를 사용하고 함수는 None을 반환하게 될 것입니다. 
# 하지만 이 경우 future.result()를 호출했을 때 반환되는 값이 None이므로 
# 이 값을 출력하려고 하면 아무것도 출력되지 않게 됩니다.