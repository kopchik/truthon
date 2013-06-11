#stdin
#stdout
#stderr
#die
main argv:[str] =
  print "hello, hell"
  print "my args:", argv
  while True:
    print "what is your name?"
    answer << stdin
    if answer ~= /[A-Z][a-z]+/:
      break
    print "think twice!"
