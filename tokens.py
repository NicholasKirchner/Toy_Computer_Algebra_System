import math

#pretty self explanatory.  "u" denotes unary negation (i.e. RPN 3 u
#gives -3)
unary_operator_tokens = ["u","sin","cos","tan","ln","arcsin","arccos","arctan","exp","D"]
#Tokens file to identify the types of operators and operands involved
#along with their properties.

binary_operator_tokens = ["+","-","*","/","^","log"]
variable_tokens = ['x']
inline_operators = ["+","-","*","/","^"]
number_types = [int,float]

#Dictionary to hold functions for operators.  Enables abstraction of
#calculations.
operations = {"+":lambda x,y: x+y,
              "-":lambda x,y: x-y,
              "*":lambda x,y: x*y,
              "/":lambda x,y: float(x)/y,
              "^":lambda x,y: x**y,
              "u":lambda x: -x,
              "log":lambda x,y:math.log(y,x), #Note: first argument is
              #the base.
              "sin":math.sin,
              "cos":math.cos,
              "tan":math.tan,
              "ln":lambda x:math.log(x),
              "arcsin":math.asin,
              "arccos":math.acos,
              "arctan":math.atan,
              "exp":math.exp}

#First element is order of evaluation, second is precedence, third is
#associativity.  This is needed for conversion between infix and
#RPN/tree representations of expressions.
binary_operations_data = {"+":["left",1,1],
                          "-":["left",1,0],
                          "*":["left",2,1],
                          "/":["left",2,0],
                          "^":["right",3,0]}
