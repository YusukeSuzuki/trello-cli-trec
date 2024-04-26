def name():
  return 'archive'

def help():
  return 'archive list'

def implement(parser):
  parser.add_argument('--board', '-b')
  parser.add_argument('list')

def process(args):
  print('archive list of board(TBI)')
