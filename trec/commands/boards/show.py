import re

import yaml
import jmespath

import trec.data as data
import trec.utils.trello as trello_util
from trec.utils.api_keys import from_args as keys_from
from trec.utils.jmespath import options as jmespath_options

def name():
  return 'show'


def help():
  return 'show board detail'


def implement(parser):
  parser.add_argument('name', help='name of board or trello id (wildcard available)')
  parser.add_argument('--full', action='store_true', help='dump full yaml of board')


def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  id_query_parameter = trello_util.from_id_notation_to_query(args.name)

  if id_query_parameter is None:
    query = f"[].boards[?name=='{args.name}'][]"
  else:
    query = f"[].boards[?fnmatch(id, '{id_query_parameter}')]"

  if not args.full:
    query += ('''
      .{
        name: name, id: id,
        dateLastActivity: dateLastActivity,
        lists: lists[].join(' ', [to_string(id), name]) 
      }
      ''')

  boards = jmespath.search(query, db, options=jmespath_options)

  print(yaml.dump(boards, allow_unicode=True, sort_keys=False))
