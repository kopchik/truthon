#!/usr/bin/env python3
from llvm.core import Module, Constant, Type, Function, Builder, FCMP_ULT

PTR = lambda t: Type.pointer(t)
Int8  = Type.int(8)
Int32 = Type.int(32)
Int64 = Type.int(64)
Void  = Type.void()
STR   = PTR(Int8)
STRArray = PTR(STR)

class STRList:
  type = None
  def __init__(self, size):
    # assert all(type(v) == type(values[0]) for v in values), \
      # "all elements of list should be of the same type"
    self.size = size

  def codegen(self):
    self.type = Type.struct([Int64, STRArray])  #size


class Fun:
  args = None
  ret  = None
  name = "noname"

  def codegen(self):
    global module
    if not self.ret:
      ret = Void
    argc = Int32
    argv =  STRArray
    proto = Type.function(ret, [argc, argv])
    function = Function.new(module, proto, self.name)
    entry = function.append_basic_block("entry")
    exit  = function.append_basic_block("exit")


def argv(func):
  blk = func.append_basic_block("args")


class MainFun:
  def codegen(self):
    global module
    ret = Int32
    argc = Int32
    argv = STRArray
    proto = Type.function(ret, [argc, argv])
    function = Function.new(module, proto, "main")
    blk = function.append_basic_block("entry")
    builder = Builder.new(blk)
    builder.ret(Constant.int(Int32, 0))


def codegen(tree, name="(no name)", output="/tmp/llvm.ir"):
  global module
  module = Module.new(name)
  function = MainFun()
  function.codegen()
  print(module)
