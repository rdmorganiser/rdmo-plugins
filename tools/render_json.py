#!/usr/bin/env python3
import json
from pathlib import Path

import yaml

BASE_PATH = Path().cwd()

RDMORGANISER_PATH = BASE_PATH / 'data' / 'rdmorganiser.yaml'
SHARED_PATH = BASE_PATH / 'data' / 'shared.yaml'

OUTPUT_PATH = BASE_PATH / 'plugins.json'

def load_data(path):
    return [
        {
            'title': row.get('title', ''),
            'url': row.get('url', ''),
            'maintainer': row.get('maintainer') or '',
            'status': row.get('status', ''),
            'type': row.get('type') or [],
            'description': (row.get('description') or '').strip()
        }
        # skip hidden entries, like in the README
        for row in yaml.safe_load(path.read_text(encoding='utf-8')) or []
        if not row.get('hidden')
    ]

data = {
    'rdmorganiser': load_data(RDMORGANISER_PATH),
    'shared': load_data(SHARED_PATH)
}

OUTPUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
