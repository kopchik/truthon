#!/usr/bin/env python3

import re

class NoMatch(Exception):
  pass


class Grammar:
  def __add__(self, other):
    if isinstance(self, ALL):
      self.things += [other]
      return self
    return ALL([self, other])

  def __or__(self, other):
    if isinstance(self, OR):
      self.things += [other]
      return self
    return OR([self, other])


class RE(Grammar):
  def __init__(self, pattern, comment=None):
    self.comment = comment
    self.pattern_orig = pattern
    self.pattern = re.compile("\s*(%s)\s*"%pattern)

  def parse(self, text, pos=0):
    m = self.pattern.match(text[pos:])
    if not m:
      raise NoMatch("syntax error", text, pos)
    print(m.groups())
    return (self, m.groups()[0]), pos+m.end()

  def __repr__(self):
    if self.comment:
      return self.comment
    cls = self.__class__.__name__
    # return "%s(\"%s\")" % (cls, self.pattern_orig)
    return "%s" % (cls)



class OR(Grammar):
  """ First match wins
  """
  def __init__(self, things):
    self.things = things

  def parse(self, text, pos=0):
    for thing in self.things:
      try:
        return thing.parse(text, pos)
      except NoMatch:
        pass
    raise NoMatch("syntax error", text, pos)


class SOMEOF(Grammar):
  def __init__(self, things):
    self.things = things

  def parse(self, text, pos=0):
    result = []
    while True:
      for thing in self.things:
        try:
          r, pos = thing.parse(text, pos)
          result += [r]
          break  # break is neccessary because it's a PEG parser and order does matter
        except NoMatch:
          pass
      else:
        break
    if not result:
      raise NoMatch("syntax error", text, pos)
    return result, pos


ENDL = RE(r'$')

class Composer(Grammar):
  def __init__(self, things):
    self.things = things

class MAYBE(Composer):
  def parse(self, text, pos=0):
    oldpos = pos
    result = OrderedDict()
    try:
      for thing in self.things:
        r, pos = thing.parse(text, pos)
        result.update(r)
    except NoMatch:
      return {}, oldpos
    return result, pos


class ALL(Composer):
  def parse(self, text, pos=0):
    result = OrderedDict()
    for thing in self.things:
      r, pos = thing.parse(text, pos)
      result.update(r)
    return result, pos


class SYMBOL(RE):
  def __init__(self, symbol):
    super().__init__(re.escape(symbol))


if __name__ == '__main__':
  INTCONST = RE(r'[-]{0,1}\d+')
  print(INTCONST.parse("-1"))
