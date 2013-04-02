Truthon
=======

My experiments with compilers, do not use!


FILES
-----

bnf.py      -- engine to define grammar in a bnf-like way
grammar.py  -- formal grammar definition
ast.py      -- abstract syntax tree nodes
expr.py     -- expression parses
type.py     -- type checker

Stages
------

1. Indent parse
1. Formal grammar parsing
1. Expression parsing
1. Type validation
1. Code generation
1. asm generation
1. Compile and link


Goals
-----

1. Tries to be safe and friendly
1. Static typing
1. Python-like syntax
1. Public/Protected/Private attributes of the classes
1. Built-in regexp support
1. Built-in shell commands invocation
1. Function overloading
1. Custom operators
1. Garbage collection
1. Will alarm on useless statements (like forget to call function)
1. Substitute vars in strings: "Hello, ${username}!"
1. UTF8 strings
1. C-style ternary condition operator
1. Assigments in if-clause (but it should evaluate to bool <- safety measure)
1. Support comments:
    shell-style # blah
    cpp // here is the comment
    C /* Hi! */
1. All programs can be opened as libraries
1. No header files needed, everything is in elf (possibly in compressed format).



Types:
  Start with capital letter

Why static:
  Just today I found typing bugs in pypeg and modgrammar. I see typing
  problems almost every day in many programs and libraries!

Future:
    pattern matching
    ADT??

Changes from python:
  No tabs allowed for indentation

Comparing to C:
  better support for variable number of arguments (you know the number
  of passed arguments, you can access them via normal array)

Translator design:
  Top-down PEG parser because it's simple.
  1. Ident parser
  2. Regexp parser
  3. AST composer

TODO:
  wildcard syntax? def X(*things)


Phases:
  1. Indent parsing
    Parses source into tree with scopes defined
    by indentation (python-like).
  2. Grammar parsing
    Build abstract syntax tree over the previous tree.
    It's ``top-down'' parser.
  3. Translation to llvm intermediate representation.
    AST traversing and code generation.
  4. Sanity check
    Checks that, e.g., main() has correct arguments and so on.
  5. Assembler invocation
    Final phase to build the program.




Project name:
  1. brainduck (busy)