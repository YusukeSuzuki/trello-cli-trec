from typing import Any, Dict, Optional

import requests

def organizations(
  user_id: str='me', *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  url = f'https://api.trello.com/1/members/{user_id}/organizations'
  headers = { 'Accept': 'application/json' }
  query = { 'key': api_key, 'token': api_token }
  response = requests.request('GET', url, headers=headers, params=query)
  user_organizations = response.json()

  return user_organizations
