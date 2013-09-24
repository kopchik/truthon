#!/usr/bin/env python3

from pratt import Value
from peg import RE, SOMEOF, ENDL, MAYBE, S
from ast import symap

# CONSTANTS
FLOATCONST = RE(r'[-]{0,1}\d+\.\d*')
INTCONST = RE(r'[-]{0,1}\d+')
STRCONST = RE(r'"(.*)"')
CONST = FLOATCONST | INTCONST | STRCONST


# COMMENTS
SHComment  = RE(r'\#.*')
CPPComment = RE(r'//.*')
CComment   = RE(r'/\*.*?\*/')
COMMENT = SHComment | CComment | CPPComment
# END is like ENDL (end of line)
# but allows trailing comments
END = MAYBE(COMMENT) + ENDL

# IDENTIFIER (FUNCTION NAMES, ETC)
ID = RE(r'[A-Za-z_][a-zA-Z0-9_]*')



def tokenize(s):
  OP = S("<bootstrap>")
  # sort by size is necessary for PEG parsers
  # because first match wins.
  for sym in sorted(symap.keys(), key=len, reverse=True):
    OP = OP | S(sym)
  PROG = SOMEOF(CONST, OP, ID, COMMENT)

  parser = PROG()
  r, pos = parser.parse(s)
  print(r)
  tokens = []
  for t,v in r:
    v = v.strip()  #TODO: fix peg
    if v in symap: tokens += [symap[v]()]
    else:          tokens += [Value(v)]
  return tokens
