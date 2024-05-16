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
  return 'create new board'


def implement(parser):
  parser.add_argument('--in', dest='in_', type=str, required=False, default=None,
    help='workspace name or id where boards should be in. default is first found workspace')
  parser.add_argument('--description', type=str, required=False, default=None,
    help='description of board')
  parser.add_argument('name', help='name of board')
  parser.add_argument('--dump', action='store_true', help='dump data into stdout')


def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  if args.in_ is not None:
    ws_id_query_parameter = trello_util.from_id_notation_to_query(args.in_)

    if ws_id_query_parameter is not None:
      query = f"[?fnmatch(id, '{ws_id_query_parameter}')][]"
    else:
      query = f"[?displayName=='{args.in_}'][]"
    ws_list = jmespath.search(query, db, options=jmespath_options)

    if len(ws_list) > 1:
      raise ValueError(f'destination list spec is ambigous: {args.in_}')
    elif not ws_list:
      raise ValueError(f'destination list is not found: {args.in_}')

    idOrganization = ws_list[0]['id']
  else:
    idOrganization = None

  created_board = api.boards.create(
    args.name,
    description=args.description,
    idOrganization=idOrganization,
    **keys_from(args))

  if args.dump:
    print(yaml.dump(created_board, allow_unicode=True))
