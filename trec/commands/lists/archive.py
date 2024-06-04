import jmespath

import trec.api as api
import trec.data as data
import trec.utils.trello as trello_util
from trec.utils.api_keys import from_args as keys_from
from trec.utils.jmespath import options as jmespath_options


def name():
  return 'archive'

def help():
  return 'archive all cards in list'

def implement(parser):
  parser.add_argument('list')
  parser.add_argument('--dump', action='store_true', help='dump data into stdout')

def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  list_query_string = trello_util.query_for_list(args.list)
  lists = jmespath.search(list_query_string, db, options=jmespath_options)

  if not lists:
    print('there is no target list')
    return

  responses = []

  for target_list in lists:
    response = api.lists.archive_all(target_list['id'], **keys_from(args))
    responses.append(response)

  if args.dump:
    print(yaml.dump(responses, allow_unicode=True))
