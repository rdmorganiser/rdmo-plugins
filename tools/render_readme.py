#!/usr/bin/env python3
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BASE_PATH = Path().cwd()

RDMORGANISER_PATH = BASE_PATH / 'data' / 'rdmorganiser.yaml'
SHARED_PATH = BASE_PATH / 'data' / 'shared.yaml'

TEMPLATE_PATH = BASE_PATH / 'templates' / 'README.md'
OUTPUT_PATH = BASE_PATH / 'README.md'

env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH.parent),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)

markdown = env.get_template(TEMPLATE_PATH.name).render(
    rdmorganiser=yaml.safe_load(RDMORGANISER_PATH.read_text(encoding='utf-8')),
    shared=yaml.safe_load(SHARED_PATH.read_text(encoding='utf-8'))
)

Path(OUTPUT_PATH).write_text(markdown, encoding='utf-8')
