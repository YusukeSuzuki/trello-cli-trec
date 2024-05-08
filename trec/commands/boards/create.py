from functools import reduce

import requests
import yaml

import trec.api as api


def name():
  return 'create'


def help():
  return 'create new board'


def implement(parser):
  parser.add_argument('--target', '-t', type=str, required=False, default=None,
    help='target workspace workspace. default is first found workspace')
  parser.add_argument('--description', type=str, required=False,
    help='name of card')
  parser.add_argument('name', help='name of card')


def process(args):
  created_board = api.boards.create(**vars(args))
  print(yaml.dump(created_board, allow_unicode=True))
