import socket
import ipaddress

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

def get_subnet_info(ip):
    subnet_mask = '255.255.255.0'
    network = ipaddress.ip_network(f'{ip}/{subnet_mask}', strict=False)
    return network

def main():
    local_ip = get_local_ip()
    network = get_subnet_info(local_ip)
    print(f'Local IP: {local_ip}')
    print(f'Subnet Mask: {network.netmask}')
    print(f'Network Range: {network}')

if __name__ == '__main__':
    main()
