from typing import Any, Dict, Optional

import requests

def boards(
  organization_id: str, *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  url = f'https://api.trello.com/1/organizations/{organization_id}/boards'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  response = requests.request('GET', url, headers=headers, params={ 'lists': 'all', **query })
  boards = response.json()

  return boards 
