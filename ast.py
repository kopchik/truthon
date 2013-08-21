#!/usr/bin/env python3

from collections import defaultdict

def factory():
  class Op:
    lbp = None
    rbp = None
    sym = None
    def nud(self, expr):
      """ null denotation (starting token) """
      raise Exception("this token cannot start expr")

    def led(self, left, expr):
      """ left denotation """
      raise Exception("this token cannot be in the middle of expr")
    def __repr__(self):
      cls = self.__class__.__name__
      return "%s(%s<'%s'>%s)" % (cls, self.lbp, self.sym, self.rbp)
  return Op
symap = defaultdict(factory)


class prefix:
  def __init__(self, sym, rbp):
    self.sym = sym
    self.rbp = rbp

  def __call__(self, cls):
    op = symap[self.sym]
    def nud(self, expr):
      print(self)
      return cls(expr(self.rbp))
    op.nud = nud
    op.rbp = self.rbp
    op.sym = self.sym
    return cls


class infix:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp

  def __call__(self, cls):
    op = symap[self.sym]
    def led(self, left, expr):
      return cls(left, expr(self.lbp))
    op.led = led
    op.sym = self.sym
    op.lbp = self.lbp
    return cls


class Value:
  lbp = 0
  def __init__(self, value):
    self.value = value
  def nud(self, expr):
    return self
  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, self.value)


class END:
  lbp = 0
  def __repr__(self):
    return "END"

#--
class Binary:
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s %s)" % (cls, self.left, self.right)

class Unary:
  def __init__(self, value):
    self.value = value
  def __repr__(self):
    cls = self.__class__.__name__
    return "(%s %s)" % (cls, self.value)

@prefix('-', 100)
class Minus(Unary):
  pass

@prefix('+', 100)
class Plus(Unary):
  pass

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
      print(cur, nxt)
      left = cur.led(left, expr)
    return left

def tokenizer(s):
  tokens = s.split()
  for t in tokens:
    if t in symap:
      yield symap[t]()
    else:
      yield Value(t)
  yield END()

def main():
  tokens = tokenizer("1 + 2 + 3")
  # print(list(tokens))
  # tokens =  symap['-'](), Value(1), symap['+'](), Value(2), END()
  # tokens = symap['-'](), Value(1), END()
  expr = Expr(tokens)
  print(expr.expr())


if __name__ == '__main__':
  main()