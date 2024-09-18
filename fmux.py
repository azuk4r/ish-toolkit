#!/usr/bin/env python3
from threading import Thread, Event
from subprocess import Popen, PIPE
from colorama import Fore, Style
from os import chdir, getcwd
from time import sleep
from sys import stdout

stop_event = Event()

def run_command(command):
	if command.startswith('cd '):
		try:
			directory = command.split(' ', 1)[1]
			chdir(directory)
			output = '\nChanged directory to: ' + getcwd() + '\n'
		except Exception as e:
			output = '\nError changing directory: ' + str(e) + '\n'
		stdout.write(output)
		stdout.flush()
	else:
		process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True, encoding='utf-8', errors='replace')
		for output in process.stdout:
			stdout.write(output)
			stdout.flush()
		for error_output in process.stderr:
			stdout.write(error_output)
			stdout.flush()

def read_input():
	while not stop_event.is_set():
		stdout.write(f'{Fore.RED}fmux>{Style.RESET_ALL} ')
		stdout.flush()
		command = input()
		if command.strip() == 'exit' or command.strip() == 'q':
			stop_event.set()
		else:
			Thread(target=run_command, args=(command,)).start()

def main():
	Thread(target=read_input, daemon=True).start()
	while not stop_event.is_set():
		sleep(1)

if __name__ == '__main__':
	main()
