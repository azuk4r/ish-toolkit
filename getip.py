#!/usr/bin/env python3
from colorama import Fore, Style
from sys import argv, exit
from requests import get
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
		print(f'{Fore.YELLOW}[getip]{Style.RESET_ALL} {target} ip: {target_ip}')
		exit(1)
	except error as e:
    		print(f'{Fore.YELLOW}[getip]{Style.RESET_ALL} error: {e}')
    		exit(1)

# get public ip and connection port
try:
	target_ip=gethostbyname(target)
	s=socket(AF_INET,SOCK_DGRAM)
	s.connect((target_ip,80))
	local_ip=s.getsockname()[0]
	public_ip=get('https://ifconfig.me').text
	print(f'{Fore.YELLOW}[getip]{Style.RESET_ALL} my local ip: {local_ip}')
	print(f'{Fore.YELLOW}[getip]{Style.RESET_ALL} my public ip: {public_ip}')
	s.close()
except error as e:
	print('{Fore.YELLOW}[getip]{Style.RESET_ALL} error: {e}')
