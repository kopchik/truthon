from ast import Node, Leaf, Eq, Lambda, Print as ASTPrint, rewrite
from frame import Frame
from log import Log
log = Log("interpreter")


class Func(Node):
  fields = ['args', 'body']

  def run(self, frame):
    return self.body.run(frame)


class Print(Node):
  fields = ['arg']
  def run(self, frame):
    print(self.arg)
    return self.arg


class Int(Leaf):
  fields = ['value']
  def run(self, frame):
    return int(self.value)


class Array(Leaf):
  fields = ['value']
  def run(self, frame):
    return self.value

def parse_funcs(node, depth):
  if not isinstance(node, Lambda):
    return node
  node = Func(node.args, node.body)
  return node


def parse_print(node, depth):
  if not isinstance(node, ASTPrint):
    return node
  return Print(node.value)


def populate_top_frame(node, depth, frame):
  if depth == 0 and isinstance(node, Eq):
    key   = str(node.left)
    value = node.right
    frame[key] = value
  return node


def run(ast, args=[]):
  frame = Frame()
  ast = rewrite(ast, parse_funcs)
  ast = rewrite(ast, parse_print)
  log.final_ast("the final AST is:\n", ast)
  ast = rewrite(ast, populate_top_frame, frame=frame)
  log.topframe("the top frame is\n", frame)

  with frame as newframe:
    func = newframe['main']
    newframe['argc'] = Int(len(args))
    newframe['argv'] = Array(args)
    print(newframe)
    func.run(newframe)