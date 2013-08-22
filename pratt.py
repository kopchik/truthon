#!/usr/bin/env python3
# import sys; sys.setrecursionlimit(30)
from useful.mstring import s

class Op:
  lbp = None  # left binding power (left-to-right precedence)
  rbp = None  # right binding power
  def nud(self):
    """ null denotation (starting token) """
    raise Exception("this token cannot start expr")

  def led(self, left):
    """ left denotation """
    raise Exception("this token cannot be in the middle of expr")


class VALUE(Op):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def nud(self):
    return self

  def __repr__(self):
    cls = self.__class__.__name__
    return "%s" % (self.value)
    # return "(%s %s)" % (cls, self.value)

class Binary:
  def __init__(self, left, right):
    self.left = left
    self.right = right
  def __repr__(self):
    cls = self.__class__.__name__
    return s("(${cls} ${self.left} ${self.right})")

class Unary:
  def __init__(self, value):
    self.value = value
  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, self.value)


class ADD(Binary): pass
class SUB(Binary): pass
class POS(Unary): pass
class NEG(Unary): pass

class PLUS(Op):
  lbp = 10
  rbp = 100
  def nud(self):
    return POS(expr(self.rbp))
  def led(self, left):
    right = expr(self.lbp)
    print("was in led", left, right)
    return ADD(left, right)
  def __repr__(self):
    return "PLUS"

class MINUS(Op):
  lbp = 10
  rbp = 100
  def nud(self):
    return NEG(expr(self.rbp))
  def led(self, left):
    return SUB(left, expr(self.lbp))


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
  def __repr__(self):
    return "END"


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


#e=[VALUE(3), POWER(), VALUE(1), POWER(), VALUE(2), END()]
# e = [MINUS(), VALUE(1), PLUS(), VALUE(2), MINUS(), VALUE(3), END()]
e = [VALUE(1), PLUS(), VALUE(2), MINUS(), VALUE(3), END()]
print(parse(e))