import fnmatch

import jmespath
from jmespath import functions


class CustomFunctions(functions.Functions):
  @functions.signature({'types': ['string']}, {'types': ['string']})
  def _func_fnmatch(self, text, pattern):
    return fnmatch.fnmatch(text, pattern)


options = jmespath.Options(custom_functions=CustomFunctions())
