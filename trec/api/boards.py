from typing import Any, Dict, Optional

import requests

def create(
  name: str, *args: Any, description: str=None, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  # TODO: impl target workspace option
  url = 'https://api.trello.com/1/boards'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  query = { 'name': name, 'lists': 'open', **query }
  if description is not None:
    query = { 'desc': description, **query }
  response = requests.request('POST', url, headers=headers, params=query)

  return response.json()


def cards(
  board_id: str, *, description: str=None, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  url = f'https://api.trello.com/1/board/{board_id}/cards'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token,  }
  response = requests.request('GET', url, headers=headers, params=query)

  return response.json()
