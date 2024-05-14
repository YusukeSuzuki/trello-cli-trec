def from_args(args):
  return {k: v for k, v in vars(args).items() if k in ('api_key', 'api_token')}
