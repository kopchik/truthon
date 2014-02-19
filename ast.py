#!/usr/bin/env python3

from pratt import prefix, infix, infix_r, postfix, brackets, \
  symap, parse as pratt_parse

from useful.mstring import s
from log import Log
log = Log('ast')


#############
# TEMPLATES #
#############
class Node(list):
  fields = []

  def __init__(self, *args):
    if self.fields and len(args) != len(self.fields):
      raise Exception("Number of arguments mismatch defined fields")
    super().__init__(args)

  def __getattr__(self, name):
    assert name in self.fields, "Unknown field %s" % name
    idx = self.fields.index(name)
    return self[idx]

  def __setattr__(self, name, value):
    print("SET", name, value)
    idx = self.fields.index(name)
    self[idx] = value

  def __dir__(self):
    return self.fields

  def __repr__(self):
    cls = self.__class__.__name__
    args = ", ".join(map(repr, self))
    return "%s(%s)" % (cls, args)


class Leaf:
  def __init__(self, value):
    self.value = value
    super().__init__()

  def __repr__(self):
    cls = self.__class__.__name__
    return "%s:%s" % (cls, self.value)

  def __iter__(self):
    return iter([])

  def nud(self):
    return self


class Unary(Node):
  fields = ['value']


class Binary(Node):
  fields = ['left', 'right']


###########
# SPECIAL #
###########

class DENT(Leaf):
  pass

class Id(Leaf):
  pass

##############
# Data types #
##############

class Str(Leaf):
  pass

class Block(Node):
  def __repr__(self):
    return "%s(%s)" % (self.__class__.__name__, super().__repr__())
  __str__ = __repr__

  def nud(self):
    return self

#########
# UNARY #
#########

@prefix('-', 100)
class Minus(Unary):
  pass

@prefix('+', 100)
class Plus(Unary):
  pass

@prefix('p', 0)
class Print(Unary):
  pass

# @prefix('->', 2)
# class Lambda0(Unary):
#   pass

@postfix('!', 3)
class CALL(Unary):
  pass


##########
# BINARY #
##########

@infix('+', 10)
class Add(Binary):
  pass

@infix('-', 10)
class Sub(Binary):
  pass

@infix_r('^', 30)
class Pow(Binary):
  pass

@infix_r('=', 1)
class Eq(Binary):
  pass

@infix('->', 2)
class Lambda(Binary):
  fields = ['args', 'body']

@brackets('(',')')
class Parens(Unary):
  pass

@infix(',', 1)
class Comma(Node):
  fields = None
  """ Two and more commas in a row
      will be merged into one.
  """
  def __init__(self, left, right):
    values = []
    if isinstance(left, Comma):
      values += left + [right]
    else:
      values = [left, right]
    print(values)
    super().__init__(values)

  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, list(self))


class Var:
  def __init__(self, name, default=None):
    self.name = name
    self.default = default # default value
  def __repr__(self):

    return "%s(\"%s\")" % (self.__class__.__name__, self.name)


###############
# INTERPRETER #
###############

class Func(Node):
  fields = ['args', 'body']


#####################
# INDENTATION PARSE #
#####################



def add_implicit_dents(ast):
  c = 0
  for i,t in enumerate(ast):
    if isinstance(t, DENT):
      c = t.value
    elif hasattr(t, "sym") and t.sym == "->":
      for t in ast[i:]:
        if isinstance(t, DENT):
          if t.value > c:
            ast.insert(i+1, DENT(t.value))
          break
  return ast


def parse_blocks(ast, i=0, lvl=0):
  blks = []
  while i < len(ast):
    t = ast[i]
    if isinstance(t, DENT):
      if t.value == lvl:
        blk = []
        blks.append(blk)
      elif t.value > lvl:
        i, sub = parse_blocks(ast, i, lvl=t.value)
        blk.append([sub])
        i += 1
      elif t.value <= lvl:
        return i, blks
    else:
      blk.append(t)
    i += 1
  return i, blks


def precedence(ast):
  nodes = []
  for e in ast:
    if isinstance(e, list) and e:
      expr = precedence(e)
      if isinstance(expr, list):
        expr = pratt_parse(expr)
      nodes.append(expr)
    else:
      nodes.append(e)
  return nodes


def pretty_print(ast, lvl=0):
  prefix = " "*lvl
  for e in ast:
    if isinstance(e, list):
      pretty_print(e, lvl+1)
    else:
      print(prefix, e)
  if lvl == 0:
    print()


def rewrite(tree, f, d=0):
  for i,n in enumerate(tree):
      if isinstance(n, Node):
        n = rewrite(n, f, d+1)
      tree[i] = f(n, d)
  return tree


def add_blocks(node, depth):
  """Add blocks"""
  if isinstance(node, list):
    return Block(node)
  return node


def parse_args(node, depth):
  if not isinstance(node, Lambda):
    return node
  argnames = node.args[0][0]  # TODO: why so many nested lists?
  args = [Var(name.value) for name in argnames]
  node.args = args
  return node


def parse_functions(node, depth):
  if depth > 0:
    return node
  if not isinstance(node, Eq):
    return node
  node = Func(node.left, node.right)
  return node


def parse(tokens):
  tokens = add_implicit_dents(tokens)
  log.debug("after implicit dents:\n", tokens)

  _, ast = parse_blocks(tokens)
  log.blocks.debug("after block parser:\n", ast)

  ast = precedence(ast)
  log.blocks.info("after pratt parser:\n", ast)

  for f in [parse_args, parse_functions]:
    ast = rewrite(ast, f)
    log.rewrite.info("after: %s\n"% f.__name__, ast)

  return ast