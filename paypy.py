#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socket import socket, AF_INET, SOCK_DGRAM
from colorama import Fore, Style
from sys import exit, argv, stdout

class DownloadHandler(SimpleHTTPRequestHandler):
	def end_headers(self):
		filename=self.base_path.split('/')[-1]
		self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
		super().end_headers()

def get_local_ip():
	s=socket(AF_INET,SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	local_ip=s.getsockname()[0]
	s.close()
	return local_ip

# warn
if len(argv) != 3:
	print('usage: paypy <port> </payload/path>')
	exit(1)

# run server
port = int(argv[1])
file_path = argv[2]
DownloadHandler.base_path=file_path
local_ip=get_local_ip()
httpd=HTTPServer((local_ip,port),DownloadHandler)
print(f'{Fore.RED}[paypy]{Style.RESET_ALL} server started at: {local_ip}:{port}\n{Fore.RED}[paypy]{Style.RESET_ALL} downloadable payload: {file_path}')
stdout.flush()
httpd.serve_forever()
