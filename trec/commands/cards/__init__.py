from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree
import jmespath
import yaml

from . import create
from . import move

import trec.api as api
import trec.data as data
import trec.utils.trello as trello_util
from trec.utils.api_keys import from_args as keys_from
from trec.utils.jmespath import options as jmespath_options


sub_commands = [
  create,
  move
  ]


def name():
  return 'cards'


def help():
  return 'card operations, if no subcommand, list all cards'


def implement(parser):
  parser.add_argument('--in', dest='in_', default='*.*.*',
    help='specify board of cards to list up. name or trello id (wildcard available).')
  parser.add_argument('--exclude', default='\n\t\n\t',
    help='specify board to exclude from list. name or trello id (wildcard available).')
  parser.add_argument('--dump', action='store_true', help='dump yaml into stdout')


def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  list_query_string = trello_util.query_for_list(args.in_, args.exclude)
  lists = jmespath.search(list_query_string, db, options=jmespath_options)

  filtered_lists = []

  for card_list in lists:
    card_list = {key: card_list.get(key) for key in ('trecName', 'id')}
    cards = api.lists.cards(card_list['id'], **keys_from(args))
    if not cards:
      continue
    card_list['cards'] = [{k: card.get(k) for k in ('name', 'id')} for card in cards]
    filtered_lists.append(card_list)

  if args.dump:
    print(yaml.dump(filtered_lists, allow_unicode=True, sort_keys=False))
  else:
    console = Console()

    for card_list in filtered_lists:
      text = Text()
      text.append(f'list {card_list["id"]}\n', style='bold yellow')
      text.append(f'Name: {card_list["trecName"]}\n')
      text.append('\n')

      for card in card_list['cards']:
        text.append(f'  {card["id"]}: ', style='bold')
        text.append(f'"{card["name"]}"\n')

      console.print(text)
