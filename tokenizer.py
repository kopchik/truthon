from ast import symap, Value, END

def tokenize(s):
  tokens = s.split()
  for t in tokens:
    if t in symap:
      yield symap[t]()
    else:
      yield Value(t)
  yield END()