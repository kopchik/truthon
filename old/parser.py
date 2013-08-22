#!/usr/bin/env python3

from grammar import *
from bnf import *

EXPR = SOMEOF(VALUE, OP)

IF = K('if') + EXPR + S(':') + ENDL

if __name__ == '__main__':
  _if = IF()
  _if.parse("if +:")