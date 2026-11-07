#!/usr/bin/env python3
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from tabulate import tabulate

BASE_PATH = Path().cwd()

RDMORGANISER_PATH = BASE_PATH / 'data' / 'rdmorganiser.yaml'
SHARED_PATH = BASE_PATH / 'data' / 'shared.yaml'

TEMPLATE_PATH = BASE_PATH / 'templates' / 'README.md'
OUTPUT_PATH = BASE_PATH / 'README.md'

DOCS_URL = 'https://rdmo.readthedocs.io/en/latest/plugins/index.html'

TYPE_ANCHORS = {
    'Export': 'project-export-plugins',
    'Import': 'project-import-plugins',
    'OptionSetProvider': 'option-set-providers',
    'IssueProvider': 'issue-providers'
}

HEADERS = {
    'title': 'Plugin',
    'maintainer': 'Maintainer',
    'status': 'Status',
    'type': 'Type',
    'last_update': 'Last Update',
    'description': 'Description'
}

def load_data(path):
    data = [row for row in yaml.safe_load(path.read_text(encoding='utf-8')) if not row.pop('hidden', False)]
    for row in data:
        if url := row.pop('url', None):
            row['title'] = f'[{row.get('title', '')}]({url})'
        if (maintainer := row.get('maintainer')) and maintainer.startswith('@'):
            row['maintainer'] = f'[{maintainer}](https://github.com/{maintainer.lstrip('@')})'

        plugin_types = row.get('type') or []
        row['type'] = ', '.join(f'[{t}]({DOCS_URL}#{TYPE_ANCHORS[t]})' for t in plugin_types)

    return data

def markdown_table(rows):
    return tabulate(rows, headers=HEADERS, tablefmt='github')

env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH.parent),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)
env.filters['markdown_table'] = markdown_table

rdmorganiser = load_data(RDMORGANISER_PATH)
shared = load_data(SHARED_PATH)

markdown = env.get_template(TEMPLATE_PATH.name).render(rdmorganiser=rdmorganiser, shared=shared)

Path(OUTPUT_PATH).write_text(markdown, encoding='utf-8')
