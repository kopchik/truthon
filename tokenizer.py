#!/usr/bin/env python3

from peg import RE, SOMEOF, MAYBE, OR, SYMBOL
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

# TODO: add this to PROG
# END is like ENDL (end of line)
# but allows trailing comments
EOL = RE(r'$', "EOL")  # end of line
END = EOL | (COMMENT+EOL)

# IDENTIFIER (FUNCTION NAMES, VARIABLES, ETC)
ID = RE(r'[A-Za-z_][a-zA-Z0-9_]*', "ID")


def tokenize(s):
  # put longest operators first because for PEG first match wins
  operators = []
  for sym in sorted(symap.keys(), key=len, reverse=True):
    operators += [SYMBOL(sym)]
  OPERATOR = OR(*operators)
  PROG = SOMEOF(CONST, OPERATOR, ID, COMMENT) #+ END

  parser = PROG
  r, pos = parser.parse(s)
  tokens = []
  for t,v in r:
    if v in symap: tokens += [symap[v]()]
    else:          tokens += [Value(v)]
  return tokens