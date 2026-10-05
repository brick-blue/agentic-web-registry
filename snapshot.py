#!/usr/bin/env python3
"""
A dated snapshot of the brick.blue registry for the public dataset repository
(github.com/brick-blue/agentic-web-registry).

Follows /api/v1/agents.ndjson page by page to the end, and writes into <out>/<date>/:
  agents.ndjson.gz  every listing as the hub serves it (measured fields + operator-claimed text)
  agents.csv        one flat row per listing: the measurements, no free text
  stats.json        /api/v1/stats at the moment of the snapshot

    python3 deploy/dataset-snapshot.py <out-dir>

Reads the public API only; nothing here needs a key.
"""
import csv
import gzip
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HUB = 'https://brick.blue'
UA = 'brick-blue-dataset-snapshot/1.0 (+https://brick.blue/bot)'
COLUMNS = ['id', 'operatorId', 'kind', 'origin', 'endpoint', 'transport', 'protocolVersion', 'availability',
           'uptime', 'latencyMs', 'access', 'authSchemes', 'tools', 'cardQuality', 'verification',
           'firstSeenAt', 'lastSeenAt', 'lastCheckedAt', 'contentChangedAt']


def fetch(url):
    req = urllib.request.Request(url, headers={'user-agent': UA})
    with urllib.request.urlopen(req, timeout=180) as res:
        return res.read().decode('utf-8')


def flat(row):
    out = {}
    for col in COLUMNS:
        if col == 'tools':
            out[col] = len(row.get('skills') or [])
        elif col == 'authSchemes':
            out[col] = ' '.join(row.get('authSchemes') or [])
        else:
            value = row.get(col)
            out[col] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else ('' if value is None else value)
    return out


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else 'snapshot')
    day = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    target = out / day
    target.mkdir(parents=True, exist_ok=True)

    url, rows = f'{HUB}/api/v1/agents.ndjson', 0
    with gzip.open(target / 'agents.ndjson.gz', 'wt', encoding='utf-8') as nd, open(target / 'agents.csv', 'w', newline='', encoding='utf-8') as cf:
        writer = csv.DictWriter(cf, fieldnames=COLUMNS)
        writer.writeheader()
        while url:
            next_url = None
            for line in fetch(url).splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if 'hub' in row and 'what' in row:       # the stream's preface, not a listing
                    continue
                if 'done' in row and 'count' in row:     # the page trailer
                    next_url = None if row.get('done') else row.get('next')
                    continue
                nd.write(json.dumps(row, ensure_ascii=False) + '\n')
                writer.writerow(flat(row))
                rows += 1
            url = next_url
            print(f'{rows} listings', file=sys.stderr)

    (target / 'stats.json').write_text(fetch(f'{HUB}/api/v1/stats'))
    print(json.dumps({'date': day, 'listings': rows, 'dir': str(target)}))


if __name__ == '__main__':
    main()
