#!/usr/bin/env python3

from peg import RE, SOMEOF, ENDL, MAYBE, OR, SYMBOL
from pratt import Value
from ast import symap

# CONSTANTS
FLOATCONST = RE(r'[-]{0,1}\d+\.\d*', "FLOAT")
INTCONST   = RE(r'[-]{0,1}\d+', "INT")
STRCONST   = RE(r'"(.*)"', "STR")
CONST = FLOATCONST | INTCONST | STRCONST

# COMMENTS
SHELLCOMMENT = RE(r'\#.*')
CPPCOMMENT   = RE(r'//.*')
CCOMMENT     = RE(r'/\*.*?\*/')
COMMENT = SHELLCOMMENT | CCOMMENT | CPPCOMMENT

# END is like ENDL (end of line)
# but allows trailing comments
END = MAYBE(COMMENT) + ENDL

# IDENTIFIER (FUNCTION NAMES, VARIABLES, ETC)
ID = RE(r'[A-Za-z_][a-zA-Z0-9_]*', "ID")


def tokenize(s):
  OP = SYMBOL("<bootstrap>")
  # sort by size is necessary for PEG parsers
  # because first match wins.
  operators = []
  for sym in sorted(symap.keys(), key=len, reverse=True):
    operators += [SYMBOL(sym)]
  OPERATOR = OR(operators)
  PROG = SOMEOF([CONST, OPERATOR, ID, COMMENT])

  parser = PROG
  r, pos = parser.parse(s)
  print(r)
  tokens = []
  for t,v in r:
    if v in symap: tokens += [symap[v]()]
    else:          tokens += [Value(v)]
  return tokens