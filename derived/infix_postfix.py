#!/usr/bin/env python3

ops = ('*', '+')
prec = { "+": 0, "-": 0, "*": 1, "/": 1}
def infix_postfix(tokens):
    output = []
    stack = []
    for item in tokens:
        #pop elements while elements have lower precedence
        if item in prec.keys():
            print(item, list(prec.keys()))
            while stack and prec[stack[-1]] >= prec[item]:
                output.append(stack.pop())
            stack.append(item)
        #delay precedence. append to stack
        elif item == "(":
            stack.append("(")
        #flush output until "(" is reached
        elif item == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            #should be "("
            print(stack.pop())
        #operand. append to output stream
        else:
            output.append(item)
    #flush stack to output
    while stack:
        output.append(stack.pop())
    return output

if __name__ == '__main__':
    r=infix_postfix('( a + b ) * c'.split())
    print(r)