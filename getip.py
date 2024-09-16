#!/usr/bin/env python3
from requests import get
from sys import argv, exit
from socket import (
	gethostbyname, 
	error,
	socket,
	AF_INET,
	SOCK_DGRAM)
	
# default
target = "8.8.8.8"

# get target ip
if len(argv) == 2:
	target = argv[1]
	try:
		target_ip = gethostbyname(target)
		print(f'[getip] {target} ip: {target_ip}')
		exit(1)
	except error as e:
    		print(f'[error] {e}')
    		exit(1)

# get public ip and connection port
try:
	target_ip=gethostbyname(target)
	s=socket(AF_INET,SOCK_DGRAM)
	s.connect((target_ip,80))
	local_ip=s.getsockname()[0]
	connection_port=s.getsockname()[1]
	public_ip=get('https://ifconfig.me').text
	print(f'[getip] my local ip: {local_ip}')
	print(f'[getip] current socket port: {connection_port}')
	print(f'[getip] my public ip: {public_ip}')
	s.close()
except error as e:
	print('[error] {e}')
