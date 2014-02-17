#!/usr/bin/env python3

from pratt import prefix, infix, infix_r, postfix, brackets, \
  symap, parse as pratt_parse

from useful.mstring import s
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

class Block(list):
  def __init__(self, value=None):
    if not value:
      value = []
    super().__init__(value)

  def __repr__(self):
    return "%s(%s)" % (self.__class__.__name__, super().__repr__())

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
  """ Two and more commas in a row
      will be merged into one.
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

##################
# FORMAL GRAMMAR #
##################

from peg import RE, SOMEOF, MAYBE, OR, SYMBOL

# CONSTANTS
FLOATCONST = RE(r'[-]{0,1}\d+\.\d*', comment="FLOAT")
INTCONST   = RE(r'[-]{0,1}\d+', comment="INT")
STRCONST   = RE(r'"(.*)"', Str)
CONST = FLOATCONST | INTCONST | STRCONST

# COMMENTS
SHELLCOMMENT = RE(r'\#.*')
CPPCOMMENT   = RE(r'//.*')
CCOMMENT     = RE(r'/\*.*?\*/')
COMMENT = SHELLCOMMENT | CCOMMENT | CPPCOMMENT

# TODO: add this to PROG
# END is like ENDL (end of line)
# but allows trailing comments
EOL = RE(r'$', comment="EOL")  # end of line
END = EOL | (COMMENT+EOL)

# IDENTIFIER (FUNCTION NAMES, VARIABLES, ETC)
ID = RE(r'[A-Za-z_][a-zA-Z0-9_]*', Id)

# put longest operators first because for PEG first match wins
operators = []
for sym in sorted(symap.keys(), key=len, reverse=True):
  operators += [SYMBOL(sym, symap[sym])]
OPERATOR = OR(*operators)
PROGRAM = SOMEOF(CONST, OPERATOR, ID, COMMENT) #+ END

def tokenize(ast1):
  tokens = []
  for t in ast1:
    if isinstance(t, str):
      ts, l = PROGRAM.parse(t)
      # assert len(t) == l, "cannot parse %s" % t
      tokens += ts
    else:
      tokens += [t]
  return tokens


#####################
# INDENTATION PARSE #
#####################

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




def parse(raw):
  # PARSE OPERATORS AND DEFINITIONS
  ast = raw.splitlines()
  ast = add_dents(ast)
  log.dents.debug("after parsing indentation:\n", ast)
  ast = tokenize(ast)
  log.tokenizer.debug("after tokenizer:\n", ast)
  ast = add_implicit_dents(ast)
  log.tokenizer.debug("after implicit dents:\n", ast)
  _, ast = parse_blocks(ast)
  log.blocks.debug("after block parser:\n", ast)
  pretty_print(ast)
  ast = precedence(ast)
  log.blocks.info("after pratt parser:\n", ast)
  pretty_print(ast)
  # ast = pratt_parse(ast)
  # log.blocks.info("after pratt parse:\n", ast)
  # ast = prattparse(ast2)
  # log.pratt.debug("after parsing operators:\n", ast)
  return ast
