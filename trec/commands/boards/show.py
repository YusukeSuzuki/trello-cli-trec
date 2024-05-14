import re

import yaml
import jmespath

import trec.data as data
import trec.utils.trello as trello_util


def name():
  return 'show'


def help():
  return 'show board detail'


def implement(parser):
  parser.add_argument('name', help='name of board or trello id (wildcard available)')
  parser.add_argument('--full', action='store_true', help='dump full yaml of board')


def process(args):
  db = data.db.load_or_setup(**vars(args))

  id_query_parameter = trello_util.from_id_notation_to_query(args.name)

  if id_query_parameter is None:
    query = f"[].boards[?name=='{args.name}'][]"
  else:
    query = f"[].boards[]"

  if not args.full:
    query += ('''
      .{
        name: name, id: id,
        dateLastActivity: dateLastActivity,
        lists: lists[].{name: name, id: id}
      }
      ''')

  boards = jmespath.search(query, db)

  if id_query_parameter is not None:
    boards = list(filter(lambda x: not not re.match(id_query_parameter, x['id']), boards))

  print(yaml.dump(boards, allow_unicode=True, sort_keys=False))
