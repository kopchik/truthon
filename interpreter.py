from ast import Node, Leaf, rewrite
import ast
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
  def __init__(self, value):
    self.value = int(value)

  def __str__(self):
    return str(self.value)

  def run(self, frame):
    return self.value


class Str(Leaf):
  def __init__(self, value):
    self.value = value.strip('"')
  def __str__(self):
    return self.value
  def run(self, frame):
    return self.value


class Array(Leaf):
  fields = ['value']
  def run(self, frame):
    return self.value


def replace_nodes(node, depth):
  if isinstance(node, ast.Int):
    return Int(node.value)
  if isinstance(node, ast.Print):
    return Print(node.value)
  if isinstance(node, ast.Str):
    return Str(node.value)
  if isinstance(node, ast.Lambda):
    return Func(node.args, node.body)
  return node




def populate_top_frame(node, depth, frame):
  if depth == 0 and isinstance(node, ast.Eq):
    key   = str(node.left)
    value = node.right
    frame[key] = value
  return node


def run(ast, args=[]):
  frame = Frame()
  ast = rewrite(ast, replace_nodes)
  log.final_ast("the final AST is:\n", ast)
  ast = rewrite(ast, populate_top_frame, frame=frame)
  log.topframe("the top frame is\n", frame)

  with frame as newframe:
    func = newframe['main']
    newframe['argc'] = Int(len(args))
    newframe['argv'] = Array(args)
    print(newframe)
    func.run(newframe)