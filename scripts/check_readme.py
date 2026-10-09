#!/usr/bin/env python3
"""Validate README image paths and profile repository consistency."""
import json
import re
from pathlib import Path
root = Path(__file__).resolve().parents[1]
readme = (root / 'README.md').read_text(encoding='utf-8')
profile = json.loads((root / 'config/profile.json').read_text(encoding='utf-8'))
assert profile['username'] in readme, 'Profile username missing'
assert 'AiroDx' not in readme, 'Unverified project attribution'
for path in re.findall(r'(?:src|srcset)="(assets/[^" ]+)"', readme):
    assert (root / path).is_file(), f'Missing asset: {path}'
for p in profile['projects']:
    assert f'https://github.com/{profile["username"]}/{p["repo"]}' in readme, f'Missing project {p["slug"]}'
print('README references and local artwork OK')
