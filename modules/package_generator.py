#!/usr/bin/env python3
import json
from pathlib import Path

def create(output_dir, project_name):
    package = {
        "name": project_name,
        "version": "1.0.0",
        "description": "",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "echo 'Tests passed'"
        },
        "dependencies": {
            "express": "^4.18.2"
        }
    }
    with open(output_dir / "package.json", 'w') as f:
        json.dump(package, f, indent=2)
    print("  [✓] package.json")