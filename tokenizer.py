from peg import RE, SOMEOF, MAYBE, OR, SYMBOL
from ast import symap, Id, Int, Str, DENT
from log import Log

log = Log("tokenizer")

# CONSTANTS
FLOATCONST = RE(r'[-]{0,1}\d+\.\d*', comment="FLOAT")
INTCONST   = RE(r'[-]{0,1}\d+', Int)
STRCONST   = RE(r'"(.*)"', Str)
CONST = FLOATCONST | INTCONST | STRCONST

# COMMENTS
SHELLCOMMENT = RE(r'\#.*')
CPPCOMMENT   = RE(r'//.*')
CCOMMENT     = RE(r'/\*.*?\*/')
COMMENT = SHELLCOMMENT | CCOMMENT | CPPCOMMENT

# TODO: add this to PROG
# END is like ENDL (end of line)
# but allows trailing comments
EOL = RE(r'$', comment="EOL")  # end of line
END = EOL | (COMMENT+EOL)

# IDENTIFIER (FUNCTION NAMES, VARIABLES, ETC)
ID = RE(r'[A-Za-z_][a-zA-Z0-9_]*', Id)

# put longest operators first because for PEG first match wins
operators = []
for sym in sorted(symap.keys(), key=len, reverse=True):
  operators += [SYMBOL(sym, symap[sym])]
OPERATOR = OR(*operators)
PROGRAM = SOMEOF(CONST, OPERATOR, ID, COMMENT) #+ END


def get_indent(s):
  """Get current indent in symbols""" #TODO: Check that indent is in spaces, not tabs
  depth = 0
  for depth, c in enumerate(s):
    if not c.isspace():
      break
  return depth


def tokenize(raw):
  tokens = []
  for l in raw.splitlines():
    tokens += [DENT(get_indent(l))]
    ts, pos = PROGRAM.parse(l)
    # assert len(t) == pos, "cannot parse %s" % t
    tokens += ts
  log.debug("after tokenizer:\n", tokens)
  return tokens