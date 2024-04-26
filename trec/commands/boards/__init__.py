import requests
import yaml

def name():
  return 'boards'

def help():
  return 'board operations'

def implement(parser):
  pass

def process(args):
  url = 'https://api.trello.com/1/members/me/organizations'

  headers = { 'Accept': 'application/json' }
  query = { 'key': args.api_key, 'token': args.api_token }
  response = requests.request('GET', url, headers=headers, params=query)
  organizations = response.json()

  filtered_organizations = []

  for organization in organizations:
    organization = {k: organization.get(k) for k in ('displayName', 'id')}
    url = f'https://api.trello.com/1/organizations/{organization["id"]}/boards'
    response = requests.request('GET', url, headers=headers, params=query)
    organization['boards'] = [{k: board.get(k) for k in ('name', 'id')} for board in response.json()]
    filtered_organizations.append(organization)

  print(yaml.dump(filtered_organizations, allow_unicode=True, sort_keys=False))
