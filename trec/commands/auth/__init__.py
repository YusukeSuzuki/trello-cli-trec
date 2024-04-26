from configparser import ConfigParser
from getpass import getpass
from pathlib import Path

import appdirs

import trec.common as common

def name():
  return 'auth'

def help():
  return 'auth operations'

def implement(parser):
  pass

def process(args):
  print(args)

  print(
    'Enter your API key. If you don\'t have it, '
    'create an app using the URL below and get it.')
  print('https://trello.com/power-ups/admin')
  api_key = input('api key: ')

  auth_url = (
    f'https://trello.com/1/authorize?expiration=never&'
    f'scope=read,write,account&response_type=token&key={api_key}')
  print('Get the API token from the URL below and enter it.')
  print(auth_url)
  api_token = getpass('API token: ')
  
  config_dir_path = Path(appdirs.user_config_dir(common.APP_NAME))
  config_file_path = config_dir_path / 'config.ini'
  config = ConfigParser()

  if config_file_path.exists():
    config.read(config_file_path)

  config.set('default', 'api_key', api_key)
  config.set('default', 'api_token', api_token)
  config_dir_path.mkdir(exist_ok=True, parents=True)

  with config_file_path.open('w') as f:
    config.write(f)

  print(f'The config file was saved to {config_file_path} .')
