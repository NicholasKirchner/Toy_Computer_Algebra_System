#The main part of the program.  Grab input from user, compute.

from representations import *
from calculate import *

#TODO: implement shunting yard algorithm and get input in infix notation.

print "Hello.  I'm a primitive Computer Algebra System who can calculate derivatives.  Enter the function in RPN notation that you'd like to calculate.  For example, to see the derivative of f(x) = (sin(x))^3, type 'x sin 3 ^ D'.  The 'D' denotes derivative."

#Get user input
function_as_string = raw_input()

#Break input into tokens
function = function_as_string.split(' ')

#find numbers, convert to int or float
for index,x in enumerate(function):
    if x.isdigit():
        function[index] = int(x)
    elif x[0].isdigit():
        function[index] = float(x)

#Convert RPN to tree, simplify, write result in infix.
print tree_to_string(simplify(rpn_to_tree(function)))