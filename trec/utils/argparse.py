def add_sub_commands_from_module(base_parser, module):
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
      sub_parser.set_defaults(process=lambda args: sub_parser.print_help())
