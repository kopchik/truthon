#!/usr/bin/env python3

from pratt import prefix, infix, infix_r, postfix, brackets, \
  symap, parse as prattparse
from indent import parse_dents
from tokenizer import tokenize

from log import Log
log = Log('ast')


#############
# TEMPLATES #
#############
class Node:
  fields = []

  def __init__(self, *args):
    assert len(args) == len(self.fields), \
      "Number of arguments mismatch defined fields"
    self.list = list(args)

  def __getattr__(self, name):
    assert name in self.fields, "Unknown field %s" % name
    idx = self.fields.index(name)
    return self.list[idx]

  def __iter__(self):
    return iter(self.list)

  def __repr__(self):
    cls = self.__class__.__name__
    args = ",".join(map(repr, self.list))
    return "%s(%s)" % (cls, args)


class Unary(Node):
  fields = ['value']


class Binary(Node):
  fields = ['left', 'right']


class DENT(Node):
  def __init__(self, depth):
    self.depth = depth
    super().__init__()
  def __repr__(self):
    cls = self.__class__.__name__
    return "%s:%s" % (cls, self.depth)

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

@prefix('->', 2)
class Lambda0(Unary):
  pass

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
  pass

@brackets('(',')')
class Parens(Unary):
  pass

@infix(',', 1)
class Comma:
  """ Two and more commas in a row will be
      merged into one
  """
  def __init__(self, left, right):
    self.values = []
    if isinstance(left, Comma):
      self.values += left.values + [right]
    else:
      self.values = [left, right]

  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, self.values)

def get_indent(s):
  """Get current indent in symbols"""
  depth = 0
  for depth, c in enumerate(s):
    if not c.isspace():
      break
  return depth

def add_dents(ast0):
  result = []
  for l in ast0:
    depth = get_indent(l)
    result.append(DENT(depth))
    result.append(l)
  return result

def parse(raw):
  # PARSE OPERATORS AND DEFINITIONS
  ast0 = raw.splitlines()
  ast1 = add_dents(ast0)
  log.dents.debug("after parsing indentation:\n", ast1)
  tokens = tokenize(ast1)
  log.tokenizer.debug("after tokenizer:\n", tokens)
  ast = prattparse(tokens)
  log.pratt.debug("after parsing operators:\n", ast)
  return ast
