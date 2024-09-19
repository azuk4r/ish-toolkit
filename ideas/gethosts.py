import socket
import ipaddress

network = ipaddress.ip_network('', strict=False)

results=[]

for ip in network:
	print(f'trying {ip}...')
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1)
		result = sock.connect_ex((str(ip), 80))
		if result == 0:
			results.append(result)
			print(f'active host: {ip}')
		sock.close()
	except Exception as e:
		pass

print('\nActive hosts:\n')

for result in results:
	print(result)
