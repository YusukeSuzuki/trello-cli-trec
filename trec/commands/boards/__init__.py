from pathlib import Path
import json

import appdirs
import requests
import yaml

import trec
import trec.data as data
from trec.utils.api_keys import from_args as keys_from

from . import create
from . import show


sub_commands = [
  create,
  show
  ]


def name():
  return 'boards'


def help():
  return 'board operations'


def implement(parser):
  pass


def process(args):
  db = data.db.load_or_setup(**keys_from(args))

  # TODO: use jmespath
  filtered_organizations = []

  for organization in db:
    boards = [
      f'{board["id"]} {board["name"]}' for board in organization['boards']]
    filtered_organizations.append({
      **{k: organization.get(k) for k in ('displayName', 'id')},
      'boards': boards,
      })

  print(yaml.dump(filtered_organizations, allow_unicode=True, sort_keys=False))
