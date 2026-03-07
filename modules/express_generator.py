#!/usr/bin/env python3
from pathlib import Path

def create(output_dir):
    index_js = """const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
app.get('/', (req, res) => res.json({ status: 'ok' }));
app.get('/api/users', (req, res) => res.json([{ id: 1, name: 'John' }]));
app.listen(PORT);
module.exports = app;
"""
    with open(output_dir / "src/index.js", 'w') as f:
        f.write(index_js)
    print("  [✓] src/index.js (fake Express app)")