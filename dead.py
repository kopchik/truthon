#!/usr/bin/env python3

from io import StringIO
import argparse
import sys

from tokenizer import tokenize
from cgen import preamble
from ast import parse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--show', action='store_const', const=True, default=True, help="show generated code")
  parser.add_argument('input', nargs='+')
  args = parser.parse_args()

  for ifname in args.input:
    outfname = ifname.rsplit('.', 1)[0] + '.c'
    with open(ifname) as fd:
      raw = fd.read()
      out = StringIO()
      out.write(preamble)

      for r in raw.split('\n'):
        if not r or r.isspace():
          continue
        tokens = tokenize(r)
        ast = parse(tokens)
        code = ast.codegen()
        out.write(code)
        out.write(";\n\n")


      print("wrinting to", outfname)
      with open(outfname, "w") as fd:
        out_raw  = out.getvalue()
        if args.show:
          print(out_raw)
        fd.write(out_raw)


if __name__ == '__main__':
  main()