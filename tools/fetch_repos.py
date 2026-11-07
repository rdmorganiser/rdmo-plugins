#!/usr/bin/env python3
import os
from pathlib import Path

import requests
import yaml

BASE_PATH = Path().cwd()

RDMORGANISER_PATH = BASE_PATH / 'data' / 'rdmorganiser.yaml'
SHARED_PATH = BASE_PATH / 'data' / 'shared.yaml'

ORG = 'rdmorganiser'
PREFIX = 'rdmo-plugins-'
API_URL = f'https://api.github.com/orgs/{ORG}/repos'
PER_PAGE = 100

HEADERS = {'Accept': 'application/vnd.github+json'}
if token := os.environ.get('GITHUB_TOKEN'):
    HEADERS['Authorization'] = f'Bearer {token}'

# dump None as an empty value (e.g. "type:") instead of "null"
yaml.SafeDumper.add_representer(type(None), lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:null', ''))

def fetch_repos():
    response = requests.get(API_URL, headers=HEADERS, params={
        'type': 'public',
        'per_page': PER_PAGE
    }, timeout=30)
    response.raise_for_status()
    return response.json()

def fetch_maintainer(repo):
    # the contributors are sorted by the number of commits, bots are skipped
    response = requests.get(repo['contributors_url'], headers=HEADERS, params={
        'per_page': PER_PAGE
    }, timeout=30)
    response.raise_for_status()
    if response.status_code == 204:  # empty repository
        return ''
    return next((
        f"@{contributor['login']}" for contributor in response.json()
        if contributor['type'] != 'Bot'
    ), '')

def load_data(path):
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or []
    for row in data:
        # remove the trailing newline of folded (>) descriptions
        if description := row.get('description'):
            row['description'] = description.strip()
    return data

def dump_data(path, data):
    # dump each entry on its own, so that the entries are separated by a blank line
    path.write_text('\n'.join(
        yaml.safe_dump([row], sort_keys=False, allow_unicode=True) for row in data
    ), encoding='utf-8')

def normalize_url(url):
    return url.rstrip('/').lower()

def create_entry(repo):
    return {
        'title': repo['name'].removeprefix(PREFIX),
        'url': repo['html_url'],
        'maintainer': fetch_maintainer(repo),
        'status': 'inactive' if repo['archived'] else 'active',
        'type': None,
        'description': repo.get('description') or '',
        'hidden': True
    }

rdmorganiser = load_data(RDMORGANISER_PATH)
shared = load_data(SHARED_PATH)

urls = {normalize_url(row['url']) for row in [*rdmorganiser, *shared] if row.get('url')}

new_repos = sorted((
    repo for repo in fetch_repos()
    if repo['name'].startswith(PREFIX) and normalize_url(repo['html_url']) not in urls
), key=lambda repo: repo['name'])

if new_repos:
    rdmorganiser += [create_entry(repo) for repo in new_repos]
    dump_data(RDMORGANISER_PATH, rdmorganiser)

    for repo in new_repos:
        print(f"Added {repo['html_url']}")
    print('Please fill in the type for the new entries and remove hidden to show them in the README.')
else:
    print('No new repositories found.')
