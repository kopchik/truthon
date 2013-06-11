/* DATA TYPES */
//ints and floats, types are infered from the value
i = 1; f = 1.0
// list
l = [1,2,3]
//tuple (arguments of functions are passed in tuples)
t = 1, 2, 3
//tuple with named fields
tuple X: a, b, c
x = X a=1, b=2, c=3
// the same but with optional parens
x = X(a=1, b=2, c=3)
// access tuple attrs
print x.a, x.b, x.c
//hashes
{a=>b}
{}
//regular expressions
pattern = /[A-z][a-z]{1-2}/


/* BASICS */
// define variable
x = 1

// define function "z" of two args
z x:int, y:int = 2*x + y

// function invocation
z 1, 2
// or
z x=1, y=2

// composition, equivalent of print(z(1,2))
print z 1, 2

// conditions:
if a > 2:
  pass
//if-else in one line
if x == 2: {x = 3} else: {x = 4}
//regexp
if x ~= //


switch x:
  x == 1: pass
  x < 10: print("x is really less than 10")
          continue  # go down
  x < 5 : print("x ")
  _     : print("what a strange X")


/* OOP */

# ns stands for namespace
ns MyClass:
  x = 1  # private by default
  public:
    print_x: print x
    get_x    : self.x
    set_x val: self.x = val
    property x:
      get:     self.x
      set val: self.x = val


instance = MyClass
print instance.x
print instance.get_x


/* SUGAR */

# shell invocation
x = `ps ax | wc -l`


# equivalent of vm = VM(); ...; vm.stop()
vm1 = VM(), vm2 = VM():
  on cleanup:
    vm1.stop and vm2.stop():
  ...


/* HIGHER ORDER FUNCTIONS */

# a(b(c))
c | b | a
a . b . c

/* GROUPING */
// block may appear at any place where expression is acceptable.
// the return value is the last statement
// statements are separated by semicolon.
x = true
if x: {print "it turned out that x is true"; x=false}
else: {print "x is false, sad but true"; }


/* HELLO, WORLD */
main argv =
  print "hello, hell"
  print "my args:", argv

/* STRING SUBSTITUTION */
x = 666
print "x is equal to ${x+1}" // equivalent of { tmp = x+1; printf("x is equal to %d\n", tmp) }

/* EXCEPTIONS */
// catch exception and get its value in _err
fd = open "filename" || die "exception ${_err}"

try:
  fd = open "filename"
except NotFound:
  fd = -1

fd = try {open "filename"} except NotFound: -1


/* LANGUAGE MODES */
//shell invocation in backticks
files = `ls -la /tmp`
`for f in ${files}; do scp $f remote:/tmp; done` \
  || die "scp failed with ${_err}"


/* COMMENTS */
// this is a comment
# and this is a comment
/* and this as well */
; have fun with many comment styles
