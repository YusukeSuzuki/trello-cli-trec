from functools import reduce

import requests
import yaml

def name():
  return 'create'

def help():
  return 'create card'

def implement(parser):
  parser.add_argument('--target', '-t', type=str, required=True,
    help='workspace.board.list or board.list notation')
  parser.add_argument('name', help='name of card')

def process(args):
  headers = { 'Accept': 'application/json' }
  query = { 'key': args.api_key, 'token': args.api_token,  }

  url = 'https://api.trello.com/1/members/me/boards'
  detailed_query = {
    'fields': 'id,name',
    'lists': 'open',
    **query
    }
  response = requests.request('GET', url, headers=headers, params=detailed_query)
  boards = response.json()
  def to_lists(lists, board):
    return lists + [{'targetName': f'{board["name"]}.{l["name"]}', **l} for l in board['lists']]
  lists = reduce(to_lists, boards, [])
  list_candidates = list(filter(lambda x: x['targetName'] == args.target, lists))
  
  if not list_candidates:
    print('there is no target list')
    return
  elif len(list_candidates) > 1:
    print('target list notation is ambiguous')
    print(yaml.dump(list_candidates, allow_unicode=True))
    return
  
  target_list = list_candidates[0]

  url = 'https://api.trello.com/1/cards'
  detailed_query = {
    'idList': target_list['id'],
    'name': args.name,
    **query
    }

  response = requests.request('POST', url, headers=headers, params=detailed_query)
  print(yaml.dump(response.json(), allow_unicode=True))
