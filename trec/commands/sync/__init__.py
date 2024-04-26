from pathlib import Path
import json

import appdirs
import requests
import yaml

import trec.common as common

def name():
  return 'sync'

def help():
  return 'sync remote workspaces'

def implement(parser):
  parser.add_argument('--dump', action='store_true',
    help='dump synced data into stdout')

def process(args):
  url = 'https://api.trello.com/1/members/me/organizations'

  headers = { 'Accept': 'application/json' }
  query = { 'key': args.api_key, 'token': args.api_token }
  response = requests.request('GET', url, headers=headers, params=query)
  organizations = response.json()

  for organization in organizations:
    organization_id = organization['id']
    url = f'https://api.trello.com/1/organizations/{organization_id}/boards'
    response = requests.request('GET', url, headers=headers,
      params={ 'lists': 'all', **query })
    boards = response.json()

    organization['boards'] = boards

  data_dir_path = Path(appdirs.user_data_dir(common.APP_NAME))
  data_dir_path.mkdir(exist_ok=True, parents=True)
  data_file_path = data_dir_path / 'data.json'

  with data_file_path.open('w') as f:
    f.write(json.dumps(organizations))

  if args.dump:
    from pprint import pprint as pp
    pp(organizations)
