import argparse


class MutuallyInclusive(argparse.Action):
  def __init__(self, *args, **kwargs):
    self.required_with = kwargs.pop('required_with')
    super().__init__(*args, **kwargs)

  def __call__(self, parser, namespace, values, option_string=None):
    setattr(namespace, self.dest, values)
    for required_opt in self.required_with:
      if getattr(namespace, required_opt) is None:
        parser.error(f'{option_string} requires both --{self.dest} and --{required_opt} to be specified togethera')


class MutuallyExclusive(argparse.Action):
  def __init__(self, *args, **kwargs):
    self.exclusive_with = kwargs.pop('exclusive_with')
    super().__init__(*args, **kwargs)

  def __call__(self, parser, namespace, values, option_string=None):
    if any(getattr(namespace, ex_opt) is not None for ex_opt in self.exclusive_with):
      parser.error(f"{option_string} cannot be used with --{self.exclusive_with}")
    setattr(namespace, self.dest, values)


def add_sub_commands_from_module(base_parser, module):
  def _check_args_nop(parser, args):
    pass

  sub_parsers = base_parser.add_subparsers(metavar='<subcommands>')

  for sub_command in module.sub_commands:
    sub_parser = sub_parsers.add_parser(sub_command.name(), help=sub_command.help())

    sub_command.implement(sub_parser)

    sub_commands_of_sub_command = vars(sub_command).get('sub_commands')

    if sub_commands_of_sub_command is not None:
      add_sub_commands_from_module(sub_parser, sub_command)

    if vars(sub_command).get('process'):
      sub_parser.set_defaults(process=sub_command.process)
    else:
      sub_parser.set_defaults(
        process=lambda args, _cur_parser=sub_parser: _cur_parser.print_help())

    sub_parser.set_defaults(check_args=vars(sub_command).get('check_args', _check_args_nop))
