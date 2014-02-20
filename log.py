#!/usr/bin/env python3
from functools import partial
from termcolor import colored
from copy import copy
import sys

levels = ["debug", "info", "critical"]

styles = {
  'debug': {'color': 'white'},
  'info': {'color': 'green'},
  'notice': {'color': 'green', 'attrs': ['bold']},
  'error': {'color': 'red'},
  'critical': {'color': 'red', 'attrs': ['reverse']},
}


class Filter:
  def __init__(self, verbosity="debug"):
    self.set_verbosity(verbosity)
    self.excluded = []
    self.included = []

  def set_verbosity(self, verbosity):
    self.loglevel = levels.index(verbosity)

  def include(self):
    pass

  def exclude(self):
    pass

  def test(self, verbosity, facility):
    if levels.index(verbosity) >= self.loglevel:
      return True
    return False
logfilter = Filter()


class Log:
  def __init__(self, prefix=[]):
    if isinstance(prefix, str):
        prefix = prefix.split('.')
    self.prefix = prefix
    self.path = copy(self.prefix)

  def __getattr__(self, name):
    if name in levels:
      return partial(self.log, verbosity=name)
    self.path.append(name)
    return self

  def __call__(self, *args, **kwargs):
    self.log(*args, **kwargs)

  def log(self, *msg, verbosity="debug"):
    facility = self.prefix + self.path
    if logfilter.test(verbosity, facility):
      prefix = ".".join(facility)
      prefix += " {}:".format(verbosity)
      style = styles[verbosity]
      print(colored('.'.join(self.path)+': '+" ".join(str(m) for m in msg), **style), file=sys.stderr)
      # print(prefix, *msg, file=sys.stderr)
    self.path = copy(self.prefix)


if __name__ == '__main__':
  log = Log(["test"])
  logfilter.set_verbosity("critical")
  log.test1.test2.info("haba-haba")
