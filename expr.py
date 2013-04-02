#!/usr/bin/env python3
from useful.log import Log
import sys
sys.setrecursionlimit(30)

class Op:
  lbp = None  # left binding power (left-to-right precedence)
  def nud(self):
    raise Exception("this token cannot start expr")

  def led(self, left):
    raise Exception("this token cannot be in the middle of expr")


class VALUE(Op):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def nud(self):
    right = self.value
    return right

  def __repr__(self):
    return "%s(%s)" % (self.__class__.__name__, self.value)


class PLUS(Op):
  lbp = 10
  def nud(self):
    return expr(100)
  def led(self, left):
    return left + expr(self.lbp)

class MINUS(Op):
  lbp = 10
  def nud(self):
    return -expr(100)
  def led(self, left):
    return left - expr(self.lbp)

class MULT(Op):
  lbp = 20
  def led(self, left):
    return left * expr(self.lbp)

class POWER(Op):
  lbp = 30
  rbp = 29
  def led(self, left):
    return left ** expr(self.rbp)


class END:
  lbp = 0


def shift():
  global cur, nxt, e
  cur = nxt
  nxt = e.pop(0)
  return cur, nxt


def expr(rbp=0):
  global cur, nxt
  cur, nxt = shift()
  left = cur.nud()
  while rbp < nxt.lbp:
    cur, nxt = shift()
    left = cur.led(left)
  return left


def parse(tokens):
  global cur, nxt
  cur = None
  nxt = e.pop(0)
  return expr()


e=[VALUE(3), POWER(), VALUE(1), POWER(), VALUE(2), END()]
print(parse(e))