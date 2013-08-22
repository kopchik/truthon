#!/usr/bin/env python3
from useful.mstring import s
from io import StringIO
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
    def nud(self):
      return cls(expr(rbp))
    symbol(self.sym).nud = nud
    return cls

class infix:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp

  def __call__(self, cls):
    def led(self, left):
      return cls(left, expr(self.lbp))
    symbol(self.sym, self.lbp).led = led
    return cls

class postfix:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp

  def __call__(self, cls):
    def led(self, left):
      return cls(left)
    symbol(self.sym, self.lbp).led = led
    return cls


class infix_r:
  def __init__(self, sym, lbp):
    self.sym = sym
    self.lbp = lbp

  def __call__(self, cls):
    def led(self, left):
      return cls(left, expr(self.lbp-1))
    symbol(self.sym, self.lbp).led = led
    return cls

class Value:
  lbp = 0
  def __init__(self, value):
    self.value = value
  def nud(self):
    return self
  def __repr__(self):
    cls = self.__class__.__name__
    # return "(%s %s)" % (cls, self.value)
    return "%s" % (self.value)
  def codegen(self):
    return self.value

class END:
  lbp = 0
  def __repr__(self):
    return "END"


###################
# PRATT MACHINERY #
###################

def shift():
  global nxt, e
  return nxt, next(e)

def expr(rbp=0):
  global cur, nxt
  cur, nxt = shift()
  left = cur.nud()
  while rbp < nxt.lbp:
    cur, nxt = shift()
    left = cur.led(left)
  return left

def parse(tokens):
  global cur, nxt, e
  cur = nxt = None
  e = tokens
  cur, nxt = shift()
  return expr()
