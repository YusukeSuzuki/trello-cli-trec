from typing import Optional
import re


def from_id_notation_to_query(arg: str) -> Optional[str]:
  trello_id_notation_expr = r'\~[0-9a-f*]{1,24}'
  if re.match(trello_id_notation_expr, arg):
    return arg[1:]
  return None
