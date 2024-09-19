import os
import socket
import ipaddress

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('8.8.8.8', 80))  # Conexión a IP pública para obtener IP local
		local_ip = s.getsockname()[0]
	finally:
		s.close()
	return local_ip

def get_subnet_range(ip, subnet_mask):
	net = ipaddress.ip_network(f'{ip}/{subnet_mask}', strict=False)
	return net

def ping_ip(ip):
	response = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
	return response == 0

def scan_network(network):
	active_ips = []
	for ip in network.hosts():  # Itera sobre todas las direcciones IP válidas en la subred
		if ping_ip(ip):
			active_ips.append(str(ip))
	return active_ips

def main():
	local_ip = get_local_ip()
	subnet_mask = '255.255.255.240'
	network = get_subnet_range(local_ip, subnet_mask)
	
	print(f'Local IP: {local_ip}')
	print(f'Scanning network: {network}')

	active_ips = scan_network(network)
	
	if active_ips:
		print(f'Devices found:')
		for ip in active_ips:
			print(f'Active IP: {ip}')
	else:
		print('No active devices found.')

if __name__ == '__main__':
	main()
