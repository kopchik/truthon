#!/usr/bin/env python3

from ast import prefix, infix, infix_r, postfix

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

preamble = \
"""
#include <stdio.h>
int add(int a, int b) {
  return a+b;}

int sub(int a, int b) {
  return a-b;}

"""
