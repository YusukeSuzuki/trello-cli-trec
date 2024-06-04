from typing import Any, Dict, Optional

import requests


def cards(
  list_id: str, *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  url = f'https://api.trello.com/1/lists/{list_id}/cards'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  response = requests.request('GET', url, headers=headers, params=query)
  return response.json()


def archive_all(
  list_id: str, *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  url = f'https://api.trello.com/1/lists/{list_id}/archiveAllCards'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  response = requests.request('POST', url, headers=headers, params=query)
  return response.json()
