#!/usr/bin/env python3

from io import StringIO
import argparse

from tokenizer import tokenize
from pratt import parse as prattparse
from indent import parse as indentparse, traverse
from ast import Eq, Fun, Lambda0

def main():
  parser = argparse.ArgumentParser()
  #parser.add_argument('--show', action='store_const', const=True, default=True, help="show generated code")
  parser.add_argument('input', nargs='+')
  args = parser.parse_args()

  for ifname in args.input:
    with open(ifname) as fd:
      raw = fd.read()

      # PARSE INDENTATION
      tree = indentparse(raw)
      print("\n*after parsing indent:\n", tree)

      # PARSE OPERATORS
      traverse(tree, lambda s: prattparse(tokenize(s)))
      print("\n*after parsing operators:\n", tree)

      # PARSE TOP-LEVEL FUNCTION DEFINITIONS
      def funcdef(e):
        if not isinstance(e, Eq):
          return e
        name = e.left
        body = e.right
        assert isinstance(body, Lambda0), \
          "only lambdas without args are currently supported"
        return Fun(name, None, body.value)
      traverse(tree, funcdef, depth=0)
      print("\n*after parsing top-level functions:\n", tree)

      #TODO: MERGE CODE BLOCKS
      #TODO: MAIN() args

if __name__ == '__main__':
  main()
