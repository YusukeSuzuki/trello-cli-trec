from functools import reduce

import requests
import yaml


def name():
  return 'create'


def help():
  return 'create new board'


def implement(parser):
  parser.add_argument('--target', '-t', type=str, required=False, default=None,
    help='target workspace workspace. default is first found workspace')
  parser.add_argument('--description', type=str, required=False,
    help='name of card')
  parser.add_argument('name', help='name of card')


def process(args):
  headers = { 'Accept': 'application/json' }
  query = { 'key': args.api_key, 'token': args.api_token,  }

  url = 'https://api.trello.com/1/boards'
  detailed_query = {
    'name': args.name,
    'lists': 'open',
    **query
    }
  if args.description is not None:
    detailed_query.update({ 'desc': args.description })
  response = requests.request('POST', url, headers=headers, params=detailed_query)
  print(yaml.dump(response.json(), allow_unicode=True))
