#!/usr/bin/env python

import indent
import cgen

if __name__ == '__main__':
  data = """
extern libc.printf(arg:Int32) -> Int32
def main(argc:Int32) -> Int32:
    return 1
"""
  tree = indent.parse(data)
  print(tree)
  code = cgen.codegen(tree)