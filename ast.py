#!/usr/bin/env python3

from pratt import prefix, infix, infix_r, postfix, brackets, \
  symap, parse as prattparse
from indent import parse as indentparse, traverse
from tokenizer import tokenize

from log import Log
log = Log('ast')


#############
# TEMPLATES #
#############

class Binary:
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s %s)" % (cls, self.left, self.right)


class Unary:
  def __init__(self, value):
    self.value = value
  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, self.value)


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


class Fun:
  def __init__(self, name, args, body):
    self.name = name
    self.args = args
    self.body = body

  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s (%s) %s)" % (cls, self.name, self.args, self.body)


def parse(raw):
  # PARSE INDENTATION
  ast = indentparse(raw)
  log.indent.debug("after parsing indent:", ast)

  # PARSE OPERATORS AND DEFINITIONS
  traverse(ast, lambda s: prattparse(tokenize(s)))
  log.pratt.debug("after parsing operators:", ast)

  # PARSE TOP-LEVEL FUNCTION DEFINITIONS
  def funcdef(e):
    if not isinstance(e, Eq):
      return e
    name = e.left
    body = e.right
    if isinstance(body, Lambda0):
      return Fun(name, None, body.value)
    elif isinstance(body, Lambda):
      args = body.left
      if isinstance(args, Parens):  # remove extra parens
        args = args.value
      if isinstance(args, Comma):  # unpack CSV into list
        args = args.values
      if not isinstance(args, list):  # convert single argument to a list
        args = [args]
      return Fun(name, args, body.right)
  traverse(ast, funcdef, depth=0)
  log.topfunc.debug("after parsing top-level functions:", ast)

  return ast
  #TODO: MERGE CODE BLOCKS
  #MAIN() args
  for e in ast:
    if isinstance(e, Fun) and e.name == 'main':
      break