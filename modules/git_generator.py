#!/usr/bin/env python3
from pathlib import Path

def create(output_dir):
    gitignore = """node_modules/
.env
.DS_Store
*.log
"""
    with open(output_dir / ".gitignore", 'w') as f:
        f.write(gitignore)
    print("  [✓] .gitignore")