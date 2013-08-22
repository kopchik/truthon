#!/usr/bin/env python3

from peg import *


#################
# BASE ELEMENTS #
#################

# Allowed names for variables, classes, functions ...
def ID(name):
  GRAMMAR = RE(r'(?P<%s>[A-Za-z_][a-zA-Z0-9_]*)' % name)
  return GRAMMAR
# commonly used class
NAME = ID("name")
# taken from
#http://fdik.org/pyPEG/grammar_elements.html#basic
SHComment  = RE(r'\#.*')
CPPComment = RE(r'//.*')
CComment   = RE(r'/\*.*?\*/')
COMMENT = SHComment | CComment | CPPComment
# END is like ENDL (end of line)
# but allows trailing comments
END = MAYBE(COMMENT) + ENDL
PASS = K("pass") + END


#########
# TYPES #
#########

class INT(Re):
  regexp = r'(?P<type>Int)'
  def process(self, r):
    raise Exception("No such type: ``Int''. Did you mean Int32?")

INT64 = RE(r'(?P<type>Int64)')
INT32 = RE(r'(?P<type>Int32)')
FLOAT = RE(r'(?P<type>Float)')
STR   = RE(r'(?P<type>Str)')
TYPE = INT64 | INT32 | INT | FLOAT | STR
# VOID  = CONST({'type':None})


#############
# CONSTANTS #
#############

FLOATCONST = RE(r'(?P<value>[-]{0,1}\d+\.\d*)')
INTCONST = RE(r'(?P<value>[-]{0,1}\d+)')
STRCONST = RE(r'"(?P<value>(.*))"')
CONST = FLOATCONST | INTCONST | STRCONST


###############
# EXPRESSIONS #
###############

# operators
PLUS  = RE(r'(?P<op>\+)')
MINUS = RE(r'(?P<op>-)')
MULT  = RE(r'(?P<op>\*)')
DIV   = RE(r'(?P<op>/)')
POW   = RE(r'(?P<op>\^)')

# boolean operators
EQ    = RE(r'(?P<op>==)')
GE    = RE(r'(?P<op>\>=)')
GT    = RE(r'(?P<op>\>)')
LE    = RE(r'(?P<op>\<=)')
LT    = RE(r'(?P<op>\<)')
CAST  = S('(') + TYPE + S(')')

# Order is important! GE goes before GT,
# otherwise '<=' will be matched as '<' and '='.
# The same applies for LE and LT.
OP = PLUS | MINUS | MULT | DIV | POW | EQ | GE | GT | LE | LT | CAST

# Here it's a bit tricky.
# Since expression needs recursive definition
# we define "reference" first and then populate it
VALUE = NAME | CONST
LPAREN = S("(")
RPAREN = S(")")
PARENS = LPAREN | RPAREN
EXPR = SOMEOF(VALUE, OP, PARENS)
# PARENEXPR = S("(") + EXPR + S(")")
# EXPR.things = [(VALUE | PARENEXPR) + OP + (VALUE | PARENEXPR) | \
#                (VALUE | PARENEXPR) | \
#                VALUE | \
#                EXPR
#               ]

# EXPR.things = [(VALUE|PARENEXPR)  + OP + (VALUE|PARENEXPR)]



################
# HIGHER-ORDER #
################

DEFAULT = (S('=')+VALUE) # TODO | NOVAL
ARG = NAME + S(':') + TYPE + DEFAULT
ARGS = LIST(ARG, _name="args")
RTYPE = (S('->')+TYPE) # TODO | VOID
FUNC = K('def') + NAME + S('(') + ARGS + S(')') \
        + RTYPE + S(':') + END
IF = K('if') + EXPR + S(':') + END
RETURN_CONST = K("return") + EXPR
EXTERN  = K('extern') + ID("lib") + S('.') + ID("name") \
          + S('(') + ARGS + S(')') + RTYPE + END
PROGRAM = FUNC | ASSIGMENT | IF | PASS | RETURN_CONST | EXTERN | END


if __name__ == '__main__':
  #data = """def fname(arg1:Int64) -> Int64:"""
  #p = FUNC()
  # r, p =p.parse(data)
  # print(r)
  # data = "extern libc.printf"
  # data = "2*4+(1*2)"
  data  = "(1*2)+(3*(4/(5-6)))"
  p = EXPR()
  r, pos = p.parse(data)
  if pos != len(data):
    raise Exception("parsing failed")
  print(r)