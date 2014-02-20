#!/usr/bin/env python3

from log import logfilter
from ast import parse, pretty_print
from tokenizer import tokenize
from interpreter import run
import argparse
from sys import exit

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--tokens', action='store_const', const=True, default=False, help="show tokens")
  parser.add_argument('-a', '--ast', action='store_const', const=True, default=False, help="show abstract syntax tree")
  parser.add_argument('input', help="path to file")
  parser.add_argument('cmd', nargs="*")
  args = parser.parse_args()

  with open(args.input) as fd:
    src = fd.read()
    tokens = tokenize(src)
    if args.tokens:
      print(tokens)
    ast = parse(tokens)
    if args.ast:
      pretty_print(ast)
    exit(run(ast, args.cmd))