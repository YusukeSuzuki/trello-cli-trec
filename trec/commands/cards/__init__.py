import requests
import yaml

from . import create


sub_commands = [
  create
  ]


def name():
  return 'cards'

def help():
  return 'card operations, if no subcommand, list all cards'

def implement(parser):
  parser.add_argument('--board', '-b', default=None)
  parser.add_argument('--list', '-l')

def process(args):
  headers = { 'Accept': 'application/json' }
  query = { 'key': args.api_key, 'token': args.api_token,  }

  url = 'https://api.trello.com/1/members/me/boards'
  response = requests.request('GET', url, headers=headers, params=query)
  boards = response.json()

  filtered_boards = []

  for board in boards:
    board = {k: board.get(k) for k in ('name', 'id')}

    url = f'https://api.trello.com/1/board/{board["id"]}/cards'
    response = requests.request('GET', url, headers=headers, params=query)
    board['cards'] = [{k: card.get(k) for k in ('name', 'id')} for card in response.json()]

    if not board['cards']:
      continue

    filtered_boards.append(board)
  
  print(yaml.dump(filtered_boards, allow_unicode=True, sort_keys=False))
