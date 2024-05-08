from pathlib import Path
import json

import appdirs
import requests
import yaml

import trec
import trec.utils.common as common

from . import create


sub_commands = [
  create
  ]


def name():
  return 'boards'


def help():
  return 'board operations'


def implement(parser):
  pass


def process(args):
  data_file_path = Path(appdirs.user_data_dir(common.APP_NAME)) / 'data.json'

  if not data_file_path.exists():
    args.dump = False
    trec.commands.sync.process(args)

  with data_file_path.open() as f:
    db = json.load(f)

  filtered_organizations = []

  for organization in db:
    boards = [
      {k: board.get(k) for k in ('name', 'id')} for board in organization['boards']]
    filtered_organizations.append({
      **{k: organization.get(k) for k in ('displayName', 'id')},
      'boards': boards,
      })

  print(yaml.dump(filtered_organizations, allow_unicode=True, sort_keys=False))
