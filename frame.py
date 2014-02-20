#!/usr/bin/env python3

class Frame:
  def __init__(self, parent=None):
    self.dict = {}
    self.parent = parent
    self.depth = (self.parent.depth + 1) if self.parent else 0

  def __setitem__(self, key, value):
    self.dict[key] = value

  def __iter__(self):
    return iter(self.dict)

  def __getitem__(self, key):
    try:
      return self.dict[key]
    except KeyError:
      if not self.parent:
        raise
    return self.parent[key]

  def __repr__(self):
    cls = self.__class__.__name__
    return "%s(depth=%s, %s, parent=%s)" % (cls, self.depth, self.dict, repr(self.parent))

  def __enter__(self):
    return Frame(self)

  def __exit__(self, *args):
    pass


if __name__ == '__main__':
  frame = Frame()
  frame['a'] = 1
  print(frame['a'])
  with frame as nested:
    print(nested['a'])