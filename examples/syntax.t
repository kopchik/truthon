/* COMMENTS */

# this is a comment
/* and this is a comment */
// and even this


/* BASICS */

# define variable
x = 1

# define function "z" of two args
z x,y = 2*x + y

# function invocation
z 1,2

# equivalent of print(z(1,2))
print z 1,2

#conditions:
if a > 2: pass

if x == 2:
  x = 3
else:
  x = 4


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


/* HELLO, WORLD */
main argv =
  print "hello, hell"
  print "my args:", argv