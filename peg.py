#!/usr/bin/env python

# Library to create PEG parsers.
# It consists of primitive classes like RE (regexp-match),
# ENDL (end of line), and higher-order classes like
# LIST, OR and MAYBE ...
# GUIDELINES:
#   Use ENDL to ensure there is no junk in the end

from collections import OrderedDict
import re

from useful.log import Log


WSPACE = r'\s*'


class NoMatch(Exception):
  """ when grammar failed to match input
  """
  text = None
  pos  = None
  def __init__(self, msg, text=None, pos=None):
    if text and pos is not None:
      self.text = text
      self.pos  = pos

      if pos > 5: ptr = "here {}┘".format("─"*(pos-4))
      else:       ptr = " "*(pos+1) + "└─── somewhere here"
      msg = "{msg}:\n\"{text}\"\n{ptr}\n" \
            .format(msg=msg, text=text, ptr=ptr)
    super().__init__(msg)


class Meta(type):
  """ Allows to write grammar in forms like "A+(B|C)"
      instead of "AND(A, OR(B,C))"
  """
  def __init__(self, name, bases, ns):
    pass

  def __add__(cls, other):
    if not issubclass(cls, All):
      cls = ALL(cls)
    cls.things += [other]
    return cls

  def __or__(cls, other):
    if not issubclass(cls, Or):
      cls = OR(cls)
    cls.things += [other]
    return cls

  # def __repr__(self):
  #   if hasattr(self, 'regexp'):
  #     return "<%s:%s>" % (self.name, self.regexp)
  #   elif hasattr(self, 'things'):
  #     return "<%s:%s>" % (self.name, self.things)
  #   else:
  #     print("!",dir(self))
  #   return self.__name__


class Grammar(metaclass=Meta):
  """Abstract base class"""
  log = Log("grammar")

  def parse(self, text, pos=0):
    raise NotImplementedError

  def process(self, result):
    return result


def to_plural(inst):
  return (inst.__class__.name + "s")


############################
# REGEXP-BASED EXPRESSIONS #
############################

class Re(Grammar):
  regexp = '<PLACE FOR PATTERN>'
  log = Log("re")

  def parse(self, text, pos=0):
    m = re.match(WSPACE+self.regexp+WSPACE, text[pos:])
    if not m:
      self.log.debug("no match: \"{}\" ~= \"{}\"" \
                     .format(self.regexp, text[pos:]))
      raise NoMatch("syntax error", text, pos)
    self.log.notice("\"{}\" ~= \"{}\"" \
                    .format(self.regexp, text[pos:]))
    r = self.process(m.groupdict())
    return r, pos+m.end()

  def __repr__(self):
    cls = self.__class__.__name__
    return "%s(\"%s\")" % (cls, self.regexp)


def RE(sre):
  class RE(Re):
    regexp = sre
  return RE


def K(keyword):
  """ Keyword representation
  """
  class K(Re):
    regexp = re.escape(keyword)
  return K


def S(symbol):
  """ Symbol representation. Same as K() in code,
      but semantically different (if anybody cares)
  """
  class S(Re):
    regexp = re.escape(symbol)
  return S


# Matches end of line
ENDL = RE(r'$')


#### CONST ####
class Const(Grammar):
  """ This lexeme always returns the same result
      and don't move cursor position on parsing string
  """
  result = {}
  def parse(self, text, pos=0):
    return self.result, pos


def CONST(_result):
  class CONST(Const):
    result = _result
  return CONST


############################
# HIGHER-ORDER EXPRESSIONS #
############################

#### ALL ####
class All(Grammar):
  things = []
  def parse(self, text, pos=0):
    result = OrderedDict()
    for Thing in self.things:
      thing = Thing()
      r, pos = thing.parse(text, pos)
      result.update(r)
    result = self.process(result)
    return result, pos


def ALL(*_things):
  class ALL(All):
    things = list(_things)
  return ALL


#### OR ####
class Or(Grammar):
  """ First match wins
  """
  things = []

  def parse(self, text, pos=0):
    for Thing in self.things:
      try:
        return Thing().parse(text, pos)
      except NoMatch:
        pass
    raise NoMatch("syntax error", text, pos)

def OR(*items):
  """ Match first suitable pattern in list """
  class OR(Or):
    things = list(items)
  return OR


#### LIST ####
class List(Grammar):
  """ Matches list of items separated by sep
  """
  sep = ','
  Thing = None
  result = None
  name = None

  def parse(self, text, pos=0):
    SEP = S(self.sep)
    result = []
    while True:
      try:
        thing = self.Thing()
        r, pos = thing.parse(text, pos)
        result += [r]
        _, pos = SEP().parse(text, pos)
      except NoMatch:
        name = self.name if self.name else to_plural(thing)
        return {name: result}, pos

def LIST(item, _name=None):
  class LIST(List):
    Thing = item
    name = _name
  return LIST


class Maybe(Grammar):
  things = []

  def parse(self, text, pos=0):
    oldpos = pos
    result = OrderedDict()
    try:
      for Thing in self.things:
        r, pos = Thing().parse(text, pos)
        result.update(r)
    except NoMatch:
      return {}, oldpos
    return result, pos

def MAYBE(*_things):
  class MAYBE(Maybe):
    things = _things
  return MAYBE


#### SOME OF ####
class SomeOf(Grammar):
  """ Match from min to max elements.
      After max elements it stops
  """
  things = []
  def parse(self, text, pos=0):
    result = OrderedDict()
    while True:
      for Thing in self.things:
        try:
          thing = Thing()
          r, pos = thing.parse(text, pos)
          result.update(r)
          break
        except NoMatch:
          pass
      else:
        break
    if not result:
      raise NoMatch("syntax error", text, pos)
    return result, pos


def SOMEOF(*items):
  class SOMEOF(SomeOf):
    things = items
  return SOMEOF