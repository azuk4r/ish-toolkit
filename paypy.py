#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socket import socket, AF_INET, SOCK_DGRAM
from colorama import Fore, Style
from sys import exit, argv, stdout
from time import strftime
import urllib.request

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

def get_public_ip():
	try:
		public_ip=urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf8')
		return public_ip
	except Exception as e:
		return 'Unable to fetch public IP'

# warn
if len(argv) != 3:
	print('usage: paypy <port> </payload/path>')
	exit(1)

# run server
port=int(argv[1])
file_path=argv[2]
DownloadHandler.base_path=file_path

# Listen on all interfaces (local and public)
httpd=HTTPServer(('0.0.0.0', port), DownloadHandler)
public_ip=get_public_ip()

print(f'{Fore.RED}[paypy]{Style.RESET_ALL} server started at: {public_ip}:{port}\n{Fore.RED}[paypy]{Style.RESET_ALL} downloadable payload: {file_path}')
stdout.flush()
httpd.serve_forever()
