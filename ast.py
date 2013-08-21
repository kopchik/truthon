#!/usr/bin/env python3

from collections import defaultdict


class Op:
  lbp = None
  rbp = None
  sym = None
  def nud(self):
    """ null denotation (starting token) """
    raise Exception("this token cannot start expr")

  def led(self, left):
    """ left denotation """
    raise Exception("this token cannot be in the middle of expr")
  def __repr__(self):
    cls = self.__class__.__name__
    return "%s(%s<'%s'>%s)" % (cls, self.lbp, self.sym, self.rbp)
symap = defaultdict(Op)


class prefix:
  def __init__(self, sym, rbp):
    self.sym = sym
    self.rbp = rbp
  def __call__(self, cls):
    op = symap[self.sym]
    def nud(self, expr):
      return cls(expr(self.rbp))
    op.nud = nud
    op.rbp = self.rbp
    op.sym = self.sym


class infix:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp
  def __call__(self, cls):
    op = symap[self.sym]
    def led(self, expr, left):
      return cls(left, expr(self.lbp))
    op.sym = self.sym
    op.led = led
    op.lbp = self.lbp
    print(op, led, op.led)


class Value:
  lbp = 0
  rbp = 0
  def __init__(self, value):
    self.value = value
  def nud(self, expr):
    return self
  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, self.value)


class END:
  lbp = 0

#--
class Binary:
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s %s)" % (cls, self.left, self.right)


@prefix('-', 10)
class Minus:
  def __init__(self, expr):
    self.expr = expr

@infix('+', 10)
class Add(Binary):
  pass

@infix('-', 10)
class Sub(Binary):
  pass

class Expr:
  cur = None
  nxt = None

  def __init__(self, e):
    self.e = iter(e)
    self.shift()

  def shift(self):
    self.cur = self.nxt
    self.nxt = next(self.e)
    return (self.cur, self.nxt)

  def expr(self, rbp=0):
    expr = self.expr
    cur, nxt = self.shift()
    left = cur.nud(expr)
    while rbp < nxt.lbp:
      cur, nxt = self.shift()
      left = cur.led(cur, expr, left)
    return left


def main():
  tokens = "1 - 2".split()
  tokens = symap['-'], Value(1), symap['+'], Value(2), END()
  expr = Expr(tokens)
  print(expr.expr())


if __name__ == '__main__':
  main()