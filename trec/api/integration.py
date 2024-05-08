from typing import Any, Dict, Optional

from . import members, organizations


def download_db(
  *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  my_organizations = members.organizations(api_key=api_key, api_token=api_token)

  for organization in my_organizations:
    organization_id = organization['id']
    boards = organizations.boards(organization_id, api_key=api_key, api_token=api_token)

    organization['boards'] = boards

  return my_organizations


def download_db_with_cache(
  cache: Dict[str, any], *args: Any, api_key: str, api_token: str, **kwargs: Any,
  ) -> Dict[str, any]:

  my_organizations = members.organizations(api_key=api_key, api_token=api_token)

  for organization in my_organizations:
    cached_orgs = [org for org in cache if org['id'] == organization['id']]
    if cached_orgs:
      if cached_orgs[0]['dateLastActivity'] == organization['dateLastActivity']:
        organization['boards'] = cached_orgs[0]['boards']
        continue

    organization_id = organization['id']
    boards = organizations.boards(organization_id, api_key=api_key, api_token=api_token)

    organization['boards'] = boards

  return my_organizations
