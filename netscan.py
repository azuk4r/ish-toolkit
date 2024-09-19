import socket
import os

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('8.8.8.8', 80))
		local_ip = s.getsockname()[0]
	finally:
		s.close()
	return local_ip

def get_base_ip(local_ip):
	parts = local_ip.split('.')
	base_ip = '.'.join(parts[:3])
	return base_ip

def ping_ip(ip):
	response = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
	return response == 0

def scan_network(base_ip):
	active_ips = []
	print(f'Scanning network: {base_ip}.x...')
	for i in range(1, 255):
		ip = f'{base_ip}.{i}'
		if ping_ip(ip):
			active_ips.append(ip)
	return active_ips

if __name__ == '__main__':
	local_ip = get_local_ip()
	base_ip = get_base_ip(local_ip)
	print(f'Local IP: {local_ip}')
	active_ips = scan_network(base_ip)
	if active_ips:
		print('Active devices found:')
		for ip in active_ips:
			print(f'- {ip}')
	else:
    print('No active devices found.')
