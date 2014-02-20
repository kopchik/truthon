from ast import Node, Leaf, rewrite
from frame import Frame

class Func(Node):
  fields = ['args', 'body']

def parse_functions(node, depth):
  if depth > 0 or not isinstance(node, Eq):
    return node
  node = Func(node.left, node.right)
  return node


def run(ast):
  pass