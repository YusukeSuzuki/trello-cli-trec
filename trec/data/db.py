from typing import Any, Dict, Optional
from pathlib import Path
import json

import appdirs

import trec.utils.common as common
import trec.api as api


def load_or_setup(
  *args: Any, api_key: str, api_token: str, **kwargs: Any) -> Optional[Dict[str, any]]:

  db = load(api_key=api_key, api_token=api_token)

  if db is None:
    db = data.db.setup(api_key=api_key, api_token=api_token)

  return db


def load_or_sync(
  *args: Any, api_key: str, api_token: str, **kwargs: Any) -> Optional[Dict[str, any]]:

  db = load(api_key=api_key, api_token=api_token)

  if db is None:
    db = data.db.setup(api_key=api_key, api_token=api_token)
  else:
    db = data.db.update(api_key=api_key, api_token=api_token)

  return db


def load(*args: Any, api_key: str, api_token: str, **kwargs: Any) -> Optional[Dict[str, any]]:
  data_file_path = Path(appdirs.user_data_dir(common.APP_NAME)) / 'data.json'

  if not data_file_path.exists():
    return None

  with data_file_path.open() as f:
    db = json.load(f)

  return db


def setup(*args: Any, api_key: str, api_token: str, **kwargs: Any) -> Dict[str, any]:
  db = api.integration.download_db(api_key=api_key, api_token=api_token)

  data_dir_path = Path(appdirs.user_data_dir(common.APP_NAME))
  data_dir_path.mkdir(exist_ok=True, parents=True)
  data_file_path = data_dir_path / 'data.json'

  with data_file_path.open('w') as f:
    f.write(json.dumps(db))

  return db


def update(db: Dict[str, any], api_key: str, api_token: str, **kwargs: Any) -> Dict[str, any]:
  db = api.integration.download_db_with_cache(db, api_key=api_key, api_token=api_token)

  data_dir_path = Path(appdirs.user_data_dir(common.APP_NAME))
  data_dir_path.mkdir(exist_ok=True, parents=True)
  data_file_path = data_dir_path / 'data.json'

  with data_file_path.open('w') as f:
    f.write(json.dumps(db))

  return db
