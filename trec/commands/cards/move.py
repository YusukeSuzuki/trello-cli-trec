import jmespath
import requests
import yaml

import trec.api as api
import trec.data as data
import trec.utils.trello as trello_util
import trec.utils.api_keys as api_keys_util
from trec.utils.jmespath import options as jmespath_options


def name():
  return 'move'

def help():
  return 'move card from list to list'

def implement(parser):
  parser.add_argument('--from', dest='from_', type=str, required=False,
    help='list name where card currently in')
  parser.add_argument('--to', type=str, required=True,
    help='list name where card should be in')
  parser.add_argument('name', help='name of card')

def process(args):
  db = data.db.load_or_setup(**api_keys_util.from_args(args))

  dst_list_id_query_parameter = trello_util.from_id_notation_to_query(args.to)
  if dst_list_id_query_parameter is None:
    query = f"[].boards[].lists[?name=='{args.to}'][]"
  else:
    query = f"[].boards[].lists[?fnmatch(id, '{dst_list_id_query_parameter}')][]"

  dst_lists = jmespath.search(query, db, options=jmespath_options)

  if len(dst_lists) > 1:
    raise ValueError(f'destination list spec is ambigous: {args.to}')
  elif not dst_lists:
    raise ValueError(f'destination list is not found: {args.to}')

  dst_list = dst_lists[0]

  src_list_id_query_parameter = trello_util.from_id_notation_to_query(args.from_)
  if src_list_id_query_parameter is None:
    query = f"[].boards[].lists[?name=='{args.from_}'][]"
  else:
    query = f"[].boards[].lists[?fnmatch(id, '{src_list_id_query_parameter}')][]"

  src_lists = jmespath.search(query, db, options=jmespath_options)
  print(src_lists)

  if len(src_lists) > 1:
    raise ValueError(f'source list spec is ambigous: {args.to}')
  elif not src_lists:
    raise ValueError(f'source list is not found: {args.to}')

  src_list = src_lists[0]

  return

  cards = api.lists.cards(src_list['id'], **api_keys_util.from_args(args))

  card_id_query_parameter = trello_util.from_id_notation_to_query(args.name)

  if card_id_query_parameter is None:
    query = f"[?name=='{args.name}']"
  else:
    query = f"[?fnmatch(id, '{card_id_query_parameter}')]"

  cards_list = jmespath.search(query, cards, options=jmespath_options)

  if len(cards_list) > 1:
    raise ValueError(f'card spec is ambigous: {args.name}')
  elif not src_lists:
    raise ValueError(f'card is not found: {args.name}')

  card = cards_list[0]

  api.cards.update(card['id'], list_id=dst_list['id'], **api_keys_util.from_args(args))
