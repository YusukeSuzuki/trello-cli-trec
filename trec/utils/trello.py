from typing import Optional
import re

_TRELLO_ID_NOTATION_EXPR = r'\~[0-9a-f*]{1,24}'


def is_id_notation(arg: str) -> bool:
  return bool(re.match(_TRELLO_ID_NOTATION_EXPR, '' if arg is None else arg))


def from_id_notation_to_query(arg: str) -> Optional[str]:
  if re.match(_TRELLO_ID_NOTATION_EXPR, '' if arg is None else arg):
    return arg[1:]
  return None


def query_for_list(arg: str, exclude: str='\n\t\n\t', *, sub_trec_name: str='*.*.*') -> str:
  if not arg:
    raise ValueError('empty arg cannot be list query string')

  id_query_parameter = from_id_notation_to_query(arg)

  if id_query_parameter is not None:
    return f"[].boards[].lists[?fnmatch(id, '{id_query_parameter}')][]"

  splitted_sub_trec_name = list(map(lambda x: x or '*', sub_trec_name.split('.')))
  if len(splitted_sub_trec_name) != 3:
    raise ValueError(
      f'invalid sub trec name (should be like listA.boardB.workspaceC): {sub_trec_name}')

  def _make_name(param: str) -> str:
    splitted_param = list(map(lambda x: x or '*', param.split('.')))

    names = splitted_param + splitted_sub_trec_name[len(splitted_param):]

    if len(names) != 3:
      raise ValueError(f'invalid param for list query string: {param}')

    return '.'.join(names)

  in_name, ex_name = [_make_name(param) for param in (arg, exclude)]

  return f"[].boards[].lists[?fnmatch(trecName, '{in_name}') && !fnmatch(trecName, '{ex_name}')][]"


def query_for_card(arg: str) -> str:
  if not arg:
    raise ValueError('empty arg cannot be list query string')

  id_query_parameter = from_id_notation_to_query(arg)

  if id_query_parameter:
    return f".cards[?fnmatch(id, '{id_query_parameter}')][]"

  return f".cards[?fnmatch(name, '{arg}')][]"
