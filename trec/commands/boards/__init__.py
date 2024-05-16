from pathlib import Path
import json

import appdirs
import requests
import yaml

import trec
import trec.utils.common as common

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
  # TODO: use data module
  data_file_path = Path(appdirs.user_data_dir(common.APP_NAME)) / 'data.json'

  if not data_file_path.exists():
    args.dump = False
    trec.commands.sync.process(args)

  with data_file_path.open() as f:
    db = json.load(f)

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
