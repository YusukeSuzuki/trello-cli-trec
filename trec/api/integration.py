from typing import Any, Dict, Optional

from . import lists, members, organizations


def download_db(
  *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  my_organizations = members.organizations(api_key=api_key, api_token=api_token)

  for organization in my_organizations:
    organization_id = organization['id']
    boards = organizations.boards(organization_id, api_key=api_key, api_token=api_token)

    for board in boards:
      board['trecName'] = f'{board["name"]}.{organization["displayName"]}'

      for l in board['lists']:
        l['trecName'] = f'{l["name"]}.{board["trecName"]}'
        l['cards'] = [
          {**c, 'listTrecName': l['trecName']}
          for c in lists.cards(l['id'], api_key=api_key, api_token=api_token)]

    organization['boards'] = boards

  return my_organizations


def download_db_with_cache(
  cache: Dict[str, any], *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  my_organizations = members.organizations(api_key=api_key, api_token=api_token)

  for organization in my_organizations:
    cached_orgs = [org for org in cache if org['id'] == organization['id']]
    if cached_orgs and cached_orgs[0]['dateLastActivity'] == organization['dateLastActivity']:
      organization['boards'] = cached_orgs[0]['boards']
      continue
    cached_org = cached_orgs[0] if cached_orgs else None

    boards = organizations.boards(organization['id'], api_key=api_key, api_token=api_token)

    for board_idx, board in enumerate(boards):
      cached_boards = (
        [b for b in cached_org['boards'] if b['id'] == board['id']] if cached_org else [])
      if cached_boards and cached_boards[0]['dateLastActivity'] == board['dateLastActivity']:
        boards[board_idx] = cached_boards[0]
        continue
      cached_board = cached_boards[0] if cached_boards else None

      board['trecName'] = f'{board["name"]}.{organization["displayName"]}'

      for l in board['lists']:
        l['trecName'] = f'{l["name"]}.{board["trecName"]}'
        l['cards'] = [
          {**c, 'listTrecName': l['trecName']}
          for c in lists.cards(l['id'], api_key=api_key, api_token=api_token)]

    organization['boards'] = boards

  return my_organizations
