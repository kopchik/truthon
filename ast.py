#!/usr/bin/env python3
from useful.mstring import s
import sys

symap = {}

def symbol(sym, lbp=0):
  try:
    Sym = symap[sym]
  except KeyError:
    class Sym: pass
    Sym.__name__ = 'Sym(%s)' % sym
    Sym.__repr__ = lambda _: 'Sym(%s)' % sym
    Sym.sym = sym
    Sym.lbp = lbp
    symap[sym] = Sym
  else:
    Sym.lbp = max(lbp, Sym.lbp)
  return Sym


def method(s):
    # decorator
    assert issubclass(s, symbol_base)
    def bind(fn):
        setattr(s, fn.__name__, fn)
    return bind


class prefix:
  def __init__(self, sym, rbp):
    self.sym = sym
    self.rbp = rbp

  def __call__(self, cls):
    rbp = self.rbp
    def nud(self, expr):
      return cls(expr(rbp))
    symbol(self.sym).nud = nud
    return cls

class infix:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp

  def __call__(self, cls):
    def led(self, left, expr):
      return cls(left, expr(self.lbp))
    symbol(self.sym, self.lbp).led = led
    return cls


class infix_r:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp

  def __call__(self, cls):
    def led(self, left, expr):
      return cls(left, expr(self.lbp-1))
    symbol(self.sym, self.lbp).led = led
    return cls

class Value:
  lbp = 0
  def __init__(self, value):
    self.value = value
  def nud(self, expr):
    return self
  def __repr__(self):
    cls = self.__class__.__name__
    # return "(%s %s)" % (cls, self.value)
    return "%s" % (self.value)

class END:
  lbp = 0
  def __repr__(self):
    return "END"


#####################
# SOME OP TEMPLATES #
#####################

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

#########
# UNARY #
#########

@prefix('-', 100)
class Minus(Unary):
  pass

@prefix('+', 100)
class Plus(Unary):
  pass

@prefix('p', 0)
class Print(Unary):
  pass

@prefix('->', 2)
class Lambda0(Unary):
  pass

##########
# BINARY #
##########

@infix('+', 10)
class Add(Binary):
  pass


@infix('-', 10)
class Sub(Binary):
  pass


@infix_r('^', 30)
class Pow(Binary):
  pass

@infix('=', 1)
class Eq(Binary):
  pass

@infix('->', 2)
class Lambda(Binary):
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
    self.shift()
    left = self.cur.nud(expr)
    while rbp < self.nxt.lbp:
      self.shift()
      left = self.cur.led(left, expr)
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
  #tokens = tokenizer("p x = 1 ^ 2 ^ 3 + 1")
  tokens  = tokenizer("myfunc = 1 + -> 1 + b")
  tokens = list(tokens)
  # tokens =  symap['-'](), Value(1), symap['+'](), Value(2), END()
  # tokens = symap['-'](), Value(1), END()
  expr = Expr(tokens)
  print(expr.expr())


if __name__ == '__main__':
  main()