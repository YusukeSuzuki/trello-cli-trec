from pathlib import Path
import json

import appdirs
import requests
import yaml

import trec.data as data


def name():
  return 'sync'


def help():
  return 'sync remote workspaces'


def implement(parser):
  parser.add_argument('--refresh', action='store_true', help='ignore chache and full download')
  parser.add_argument('--dump', action='store_true', help='dump synced data into stdout')


def process(args):
  db = data.db.load(**vars(args))

  if db is None or args.refresh:
    db = data.db.setup(**vars(args))
  else:
    db = data.db.update(db, **vars(args))

  if args.dump:
    print(yaml.dump(db, allow_unicode=True, sort_keys=False))
