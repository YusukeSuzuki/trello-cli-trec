from typing import Any, Dict, Optional

import requests


def create(
  list_id: str,
  name: str,
  description: Optional[str]=None,
  *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  # TODO: add options other than list_id

  url = f'https://api.trello.com/1/cards'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  query_args = {
    'name': name,
    'desc': description,
    'idList': list_id,
    }

  query.update({ k: v for k, v in query_args.items() if v is not None })

  response = requests.request('POST', url, headers=headers, params=query)
  return response.json()

def update(
  card_id: str,
  name: Optional[str]=None,
  description: Optional[str]=None,
  list_id: Optional[str]=None,
  *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  # TODO: add options other than list_id

  url = f'https://api.trello.com/1/cards/{card_id}'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  query_args = {
    'name': name,
    'desc': description,
    'idList': list_id,
    }
  query.update({ k: v for k, v in query_args.items() if v is not None })
  return requests.request('PUT', url, headers=headers, params=query)
