#!/usr/bin/env python3
from llvm.core import Module, Constant, Type, Function, Builder, FCMP_ULT

PTR = lambda t: Type.pointer(t)
Int8  = Type.int(8)
Int32 = Type.int(32)
Int64 = Type.int(64)
Void  = Type.void()
STR   = PTR(Int8)
STRArray = PTR(STR)
STRList = Type.struct([Int64, STRArray], "STRList")

# class STRList:
#   type = None
#   def __init__(self, size):
#     # assert all(type(v) == type(values[0]) for v in values), \
#       # "all elements of list should be of the same type"
#     self.size = size

#   def codegen(self):
#     self.type = STRList



def argv(func):
  global module
  blk = func.append_basic_block("args")
  builder = Builder.new(blk)
  # fn = module.get_function_named("mainargs")
  fn = LLVMFunction("mainargs", args=[Int32, STRArray], ret=PTR(STRList), m=module)
  # print(fn.type.pointee.args)
  builder.call(fn, [Int32, STRArray], "whatisit")


class MainFun:
  def codegen(self):
    global module
    func = LLVMFunction("main", [Int32, STRArray], Int32, module)
    argv(func)
    blk = func.append_basic_block("entry")
    builder = Builder.new(blk)
    builder.ret(Constant.int(Int32, 0))
    func.verify()


def LLVMFunction(name, args, ret, m):
  proto = Type.function(ret, args)
  func  = Function.new(m, proto, name)
  return func


class STDLib:
  def codegen(self):
    global module
    #[Str] => [Str]
    LLVMFunction("PrintSTRArray", args=[STRArray], ret=STRArray, m=module)
    # LLVMFunction("mainargs", args=[Int32, STRArray], ret=PTR(STRList), m=module)


def codegen(tree, name="(no name)", output="/tmp/llvm.ir"):
  global module
  module = Module.new(name)
  stdlib = STDLib()
  stdlib.codegen()

  function = MainFun()
  function.codegen()
  print(module)
