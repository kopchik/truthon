#!/usr/bin/env python3

from peg import K,S, SOMEOF

# EXPR = SOMEOF(PLUS)
class EXPR(SOMEOF(PLUS)):
  def process(self, r):
    print(r)
    return r

IF = K('if') + S(':')
class IF(IF):
  def process(self, data):
    print(data)
if __name__ == '__main__':
  # p = IF()
  # d = "if:"
  # print(p.parse(d))
  p = EXPR()
  p.parse('++')