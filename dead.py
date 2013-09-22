#!/usr/bin/env python3

from io import StringIO
import argparse
import sys

from tokenizer import tokenize
from pratt import parse

def main():
  parser = argparse.ArgumentParser()
  #parser.add_argument('--show', action='store_const', const=True, default=True, help="show generated code")
  parser.add_argument('input', nargs='+')
  args = parser.parse_args()

  for ifname in args.input:
    with open(ifname) as fd:
      raw = fd.read()

      for r in raw.split('\n'):
        if not r or r.isspace():
          continue
        tokens = tokenize(r)
        ast = parse(tokens)
        print(ast, type(ast), ast.value)

if __name__ == '__main__':
  main()
