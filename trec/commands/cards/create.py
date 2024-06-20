import jmespath
import yaml

import trec.api as api
import trec.data as data
import trec.utils.trello as trello_util
from trec.utils.api_keys import from_args as keys_from
from trec.utils.jmespath import options as jmespath_options


def name():
  return 'create'


def help():
  return 'create card'


def implement(parser):
  parser.add_argument('--in', '-i', dest='in_', type=str, required=True,
    help='list.board.workspace or list.board notation, or trello id')
  parser.add_argument('name', help='name of card')
  parser.add_argument('--dump', action='store_true', help='dump data into stdout')


def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  list_query_string = trello_util.query_for_list(args.in_)
  lists = jmespath.search(list_query_string, db, options=jmespath_options)

  if not lists:
    print('there is no target list')
    return
  elif len(lists) > 1:
    print('target list notation is ambiguous')
    print(yaml.dump([l['trecName'] for l in lists], allow_unicode=True))
    return

  target_list = lists[0]

  response = api.cards.create(target_list['id'], args.name, **keys_from(args))

  if args.dump:
    print(yaml.dump(response, allow_unicode=True))
