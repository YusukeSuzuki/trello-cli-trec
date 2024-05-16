import jmespath
import requests
import yaml

import trec.api as api
import trec.data as data
import trec.utils.trello as trello_util
from trec.utils.api_keys import from_args as keys_from
from trec.utils.jmespath import options as jmespath_options


def name():
  return 'move'


def help():
  return 'move card from list to list'


def implement(parser):
  parser.add_argument('--in', dest='in_', type=str, default='*.*.*', required=False,
    help='list name where card currently in')
  parser.add_argument('--dump', action='store_true', help='dump data into stdout')
  parser.add_argument('name', help='name of card')
  parser.add_argument('to', help='list name where card should be moved to')


def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  src_list_id_query_parameter = trello_util.query_for_list(args.in_)
  card_id_query_parameter = trello_util.query_for_card(args.name)
  cards = jmespath.search(
    src_list_id_query_parameter + card_id_query_parameter, db, options=jmespath_options)

  if not cards:
    raise ValueError(f'card spec is ambigous: {args.in_}, {args.name}')

  responses = []

  for card in cards:
    dst_list_id_query_parameter = trello_util.query_for_list(
      args.to, sub_trec_name=card['listTrecName'])
    dst_lists = jmespath.search(dst_list_id_query_parameter, db, options=jmespath_options)

    if len(dst_lists) > 1:
      raise ValueError(f'destination list spec is ambigous: {args.to}')
    elif not dst_lists:
      raise ValueError(f'destination list is not found: {args.to}')

    dst_list = dst_lists[0]

    response = api.cards.update(card['id'], list_id=dst_list['id'], **keys_from(args))
    responses.append(response)

  if args.dump:
    print(yaml.dump(responses, allow_unicode=True))
