#!/usr/bin/env python3
"""Refresh embedded video URLs and QR images from data/videos.json.

Install optional dependency first: python -m pip install 'qrcode[pil]'
"""
from pathlib import Path
import json
import base64
from io import BytesIO
from urllib.parse import urlparse
try:
    import qrcode
except ImportError:
    raise SystemExit("Install QR dependency first: python -m pip install 'qrcode[pil]'")

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / 'site/index.html',
    ROOT / 'variants/mobile-daily.html',
    ROOT / 'variants/mobile-all-unlocked.html',
    ROOT / 'variants/desktop-daily.html',
    ROOT / 'variants/desktop-all-unlocked.html',
]
items = json.loads((ROOT / 'data/videos.json').read_text(encoding='utf-8'))
if len(items) != 25 or [v['day'] for v in items] != list(range(1,26)):
    raise SystemExit('videos.json must contain exactly days 1 through 25 in order')
embedded = []
for row in items:
    url = row['url']
    if not url.startswith('https://'):
        raise SystemExit(f"Only HTTPS URLs allowed: {url}")
    im = qrcode.make(url, box_size=5, border=4)
    buf=BytesIO(); im.save(buf, format='PNG')
    payload={"day":row['day'],"url":url,
        "qr":"data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('ascii')}
    if row.get('backupUrl'):
        payload['backupUrl']=row['backupUrl']
    embedded.append(payload)
new_json=json.dumps(embedded, separators=(',',':'), ensure_ascii=False)

for path in PATHS:
    html = path.read_text(encoding='utf-8')
    marker='const VIDEOS = '
    start=html.index(marker)+len(marker)
    _,length=json.JSONDecoder().raw_decode(html[start:])
    path.write_text(html[:start]+new_json+html[start+length:],encoding='utf-8')
    print('Updated',path.relative_to(ROOT))
print('Run python scripts/validate.py before pushing')
