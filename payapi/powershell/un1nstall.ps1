$hwnd = Get-Process -Id $PID | ForEach-Object { $_.MainWindowHandle }
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    }
"@
[WinAPI]::ShowWindow($hwnd, 0)
Start-Process powershell -ArgumentList "choco uninstall openssh -y" -WindowStyle Hidden -Wait
Start-Process powershell -ArgumentList "choco uninstall nmap -y" -WindowStyle Hidden -Wait
Stop-Service sshd
Set-Service -Name sshd -StartupType 'Disabled'
$sshDir = "$HOME\.ssh"
if (Test-Path -Path $sshDir) {
    Remove-Item -Path $sshDir -Recurse -Force
}
$nmappath = 'C:\Program Files (x86)\Nmap'
$envpath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
if ($envpath -like "*$nmappath*") {
    $newPath = $envpath -replace [regex]::Escape($nmappath + ';'), ''
    [System.Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
}
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "Write-Host 'OpenSSH, Nmap, and all keys have been removed. The environment is restored.'" -WindowStyle Normal
