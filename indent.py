#!/usr/bin/env python


def get_indent(s):
  """Get current indent in symbols"""
  depth = 0
  for depth, c in enumerate(s):
    if not c.isspace():
      break
  return depth


def indent_parse(annotated, bd=0):
  """ Parse a tree. It's an ~O(N) parser :)
      bd = current block depth
      ld = current line depth
  """
  result = []
  for p,(ld,l) in enumerate(annotated):
    if ld == bd:
      l = l.strip()
      if l: result += [l]
    elif ld > bd:
      result.append(indent_parse(annotated[p:], bd=ld))
    else:
      return result
  return result


def traverse(tree, f, depth=666):
  """traverse tree produced by indent
  """
  for i,node in enumerate(tree):
    if isinstance(node, list):
      if depth > 0:
        traverse(node, f, depth-1)
    else:
      tree[i] = f(node)


def parse(text):
  "annotate each line with its indentation, then parse"
  annotated = map(lambda l: (get_indent(l), l), text.splitlines())
  annotated = list(annotated)
  tree = indent_parse(annotated)
  return tree