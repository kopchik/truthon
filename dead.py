#!/usr/bin/env python3

from log import logfilter
from ast import parse
from tokenizer import tokenize
import argparse


def main():
  parser = argparse.ArgumentParser()
  # parser.add_argument('--show', action='store_const', const=True, default=True, help="show generated code")
  parser.add_argument('input', nargs='+')
  args = parser.parse_args()

  for fname in args.input:
    with open(fname) as fd:
      src = fd.read()
      tokens = tokenize(src)
      ast = parse(tokens)

if __name__ == '__main__':
  main()