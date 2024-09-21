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
Start-Process powershell -ArgumentList "[System.Net.WebClient]::new().DownloadString('https://community.chocolatey.org/install.ps1') | Invoke-Expression" -WindowStyle Hidden -Wait
Start-Process powershell -ArgumentList "choco install nmap --params='/NoZenmap' -y" -WindowStyle Hidden -Wait
$nmappath = 'C:\Program Files (x86)\Nmap'
$envpath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
if ($envpath -notlike "*$nmappath*") {
    [System.Environment]::SetEnvironmentVariable('Path', "$envpath;$nmappath", 'Machine')
}
# pending
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "Write-Host 'PowerShell has been restarted. Dependencies installed successfully.'; # Here an alert will be sent to the PayPy server: dependencies installed" -WindowStyle Normal
