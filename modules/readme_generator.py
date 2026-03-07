#!/usr/bin/env python3
from pathlib import Path

def create(output_dir, project_name):
    readme = f"# {project_name}\n"
    with open(output_dir / "README.md", 'w') as f:
        f.write(readme)
    print("  [✓] README.md")