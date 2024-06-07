# PYTHON_ARGCOMPLETE_OK
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
from pprint import pprint as print

import appdirs
import argcomplete

from .utils.common import APP_NAME
from . import commands 
from .utils.argparse import add_sub_commands_from_module


def create_root_argument_parser():
  parser = ArgumentParser(APP_NAME)
  add_sub_commands_from_module(parser, commands)
  return parser


def main():
  config_dir_path = Path(appdirs.user_config_dir(APP_NAME))
  config_file_path = config_dir_path / 'config.ini'
  config = ConfigParser()

  if not config_file_path.exists():
    config.add_section('default')
    config.set('default', 'api_key', '')
    config.set('default', 'api_token', '')
    config_dir_path.mkdir(exist_ok=True, parents=True)
    
    with config_file_path.open('w') as f:
      config.write(f)
  else:
    config.read(config_file_path)


  parser = create_root_argument_parser()
  argcomplete.autocomplete(parser)
  args = parser.parse_args()

  if not vars(args).get('process'):
    parser.print_help()
    return 0

  args.check_args(parser, args)

  args.api_key = config.get('default', 'api_key')
  args.api_token = config.get('default', 'api_token')

  if not args.api_key or not args.api_token:
    commands.auth.process(args)

  return args.process(args)

if __name__ == '__main__':
  main()
