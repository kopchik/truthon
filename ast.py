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
  def type(self):
    return self.value.type()

@prefix('+', 100)
class Plus(Unary):
  def codegen(self):
    # left = self.left
    # ltype = left.type()
    return self.value.codegen()

@prefix('p', 0)
class Print(Unary):
  def codegen(self):
    return "printf(%s);" % self.value.codegen()

@prefix('->', 2)
class Lambda0(Unary):
  def codegen(self):
    return self.value.codegen()

@postfix('!', 3)
class CALL(Unary):
  pass


##########
# BINARY #
##########

@infix('+', 10)
class Add(Binary):
  def codegen(self):
    return "add(%s, %s)" % (self.left.codegen(), self.right.codegen())


@infix('-', 10)
class Sub(Binary):
  def codegen(self):
    return "sub(%s, %s)" % self.left.codegen(), self.right.codegen()


@infix_r('^', 30)
class Pow(Binary):
  pass

@infix_r('=', 1)
class Eq(Binary):
  def codegen(self):
    if isinstance(self.right, (Lambda, Lambda0)):
      r  = "void %s(void)\n" % self.left
      r += "{%s}" % self.right.codegen()
      return r
    else:
      return "%s = %s" % (self.left.codegen(), self.right.codegen())

@infix('->', 2)
class Lambda(Binary):
  pass



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



def tokenizer(s):
  tokens = s.split()
  for t in tokens:
    if t in symap:
      yield symap[t]()
    else:
      yield Value(t)
  yield END()

def main():
  out = StringIO()
  out.write(preamble)



  # raw = "p x = 1 ^ 2 ^ 3 + 1"
  # raw = "myfunc = 1 + -> 1 + b"
  # raw = "main = -> p \"OPA\""
  raw = \
  """
  x = 1 + 2
  main = -> p x
  """
  for r in raw.split('\n'):
    if not r or r.isspace():
      continue
    tokens = tokenizer(r)
    e = parse(tokens)
    # expr = Expr(tokenizer(r))
    # e = expr.expr()
    code = e.codegen()
    out.write(code)
    out.write(";\n\n")


  with open("/tmp/test.c", "w") as fd:
    out_raw  = out.getvalue()
    print(out_raw)
    fd.write(out_raw)

preamble = \
"""
#include <stdio.h>
int add(int a, int b) {
  return a+b;}

int sub(int a, int b) {
  return a-b;}

"""

if __name__ == '__main__':
  main()