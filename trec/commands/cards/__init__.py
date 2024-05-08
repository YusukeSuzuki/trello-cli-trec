import jmespath
import requests
import yaml

from . import create

import trec.api as api
import trec.data as data
import trec.utils.trello as trello_util


sub_commands = [
  create
  ]


def name():
  return 'cards'

def help():
  return 'card operations, if no subcommand, list all cards'

def implement(parser):
  parser.add_argument('--board', '-b', default=None,
    help='specify board of cards to list up. name or trello id (wildcard available).')
  # TODO: add list option
  # TODO: add target option (The --target option cannot be used together with the --board or --list options.)

def process(args):
  db = data.db.load_or_setup(**vars(args))

  board_id_query_parameter = (
    trello_util.from_id_notation_to_query(args.board) if args.board is not None else None)

  if args.board is not None and board_id_query_parameter is None:
    query = f"[].boards[?name=='{args.board}'][]"
  else:
    query = f"[].boards[]"

  boards = jmespath.search(query, db)
  filtered_boards = []

  if board_id_query_parameter is not None:
    boards = list(filter(lambda x: not not re.match(board_id_query_parameter, x['id']), boards))

  for board in boards:
    board = {k: board.get(k) for k in ('name', 'id')}

    cards = api.boards.cards(board['id'], **vars(args))
    board['cards'] = [{k: card.get(k) for k in ('name', 'id')} for card in cards]

    if not board['cards']:
      continue

    filtered_boards.append(board)
  
  print(yaml.dump(filtered_boards, allow_unicode=True, sort_keys=False))
