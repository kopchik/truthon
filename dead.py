#!/usr/bin/env python3
from llvmbackend import codegen
from ast import parse
import argparse


def main():
  parser = argparse.ArgumentParser()
  #parser.add_argument('--show', action='store_const', const=True, default=True, help="show generated code")
  parser.add_argument('input', nargs='+')
  args = parser.parse_args()

  for ifname in args.input:
    with open(ifname) as fd:
      raw = fd.read()
      ast = parse(raw)
      codegen(ast, name=ifname, output="./llvm.ir")

if __name__ == '__main__':
  main()
