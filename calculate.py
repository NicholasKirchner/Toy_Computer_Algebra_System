#Calculate file which performs some simplifications to a tree.

from tokens import *

#If this were made any more extensive (i.e. more algebra rules put
#in), it would probably be better to have a separate simplify function
#for each operator, as we already have with the derivative.

#This function contains the guts of the program: Essentially an RPN
#calculator which can do a bit of basic algebra.  Algorithm: if we
#have just a number or variable return it.  If we have a derivative
#operator at the top of the tree, offload it to the deriv
#function.  Otherwise, run function on child trees, do (simple)
#simplifications (i.e. compute if numbers are involved, check for
#adding 0, and the like), return simplified tree.
def simplify(tree):
    #Special case #1: just have a number or an x.
    if type(tree) in number_types or tree in variable_tokens:
        return tree
    #Special case #2: calculate the derivative:
    if tree[0] == "D":
        return deriv(tree[1][0])
    new_subs = map(simplify,tree[1])
    if all(map(lambda x: type(x) in number_types,new_subs)):
        return apply(operations[tree[0]],new_subs)
    new_tree = [tree[0],new_subs]
    #Special case #3: add 0.
    if new_tree[0] == '+' and 0 in new_tree[1]:
        non_zero = 1 - new_tree[1].index(0)
        return new_tree[1][non_zero]
    #Special case #4: subtract 0.
    if new_tree[0] == '-' and 0 == new_tree[1][1]:
        return new_tree[1][0]
    #Special case #5,6: multiplication by 0 and 1:
    if new_tree[0] == '*':
        if 0 in new_tree[1]:
            return 0
        if 1 in new_tree[1]:
            non_one = 1 - new_tree[1].index(1)
            return new_tree[1][non_one]
    #Special case #7,8,9: divide by 1, divide zero by something,
            #divide number by itself (naive, in that the same tree
            #needs to be in each place).
    if new_tree[0] == '/':
        if new_tree[1][1]==1:
            return new_tree[1][0]
        if new_tree[1][0]==0:
            return 0
        if new_tree[1][0] == new_tree[1][1]:
            return 1
    #Special case #10,11,12,13: take x**0, 1**x, x**1, 0**x (in that order, so
        #that 0**0 == 1)
    if new_tree[0] == '^':
        if new_tree[1][1]==0 or new_tree[1][0]==1:
            return 1
        if new_tree[1][1]==1:
            return new_tree[1][0]
        if new_tree[1][0]==0:
            return 0
        if new_tree[1][0]==1:
            return 1
    return new_tree


#Rather ugly little function to handle derivatives of each operation.
#Note that I eschewed special cases like D(x^n) = n*x^(n-1).
#Rather, I implemented the full power rule for D(f^g) and left
#it to the simplify function to prune things off.
def deriv(tree):
    if type(tree) in number_types:
        return 0
    if tree in variable_tokens:
        return 1
    f = tree[1][0]
    if len(tree[1]) > 1:
        g = tree[1][1]
    if tree[0] in ['+','-']:
        new_tree = [tree[0],[deriv(f),deriv(g)]]
    if tree[0] == '*':
        new_tree = ['+',[["*",[f,deriv(g)]],["*",[g,deriv(f)]]]]
    if tree[0] == '/':
        new_tree = ['/',[["-",[["*",[g,deriv(f)]],["*",[f,deriv(g)]]]],["^",[g,2]]]]
    if tree[0] == '^': #Amazingly, I typed this correctly the first
        #try.  At least, I haven't seen any errors yet...
        new_tree = ["*",[["^",[f,g]],["+",[["*",[["/",[g,f]],deriv(f)]],["*",[deriv(g),['ln',[f]]]]]]]]
    if tree[0] == 'sin':
        new_tree = ["*",[["cos",[f]],deriv(f)]]
    if tree[0] == 'cos':
        new_tree = ["*",[["u",[["sin",[f]]]],deriv(f)]]
    if tree[0] == 'tan':
        new_tree = deriv(["/",[["sin",[f]],["cos",[f]]]])
    if tree[0] == 'ln':
        new_tree = ["/",[deriv(f),f]]
    if tree[0] == 'u':
        new_tree = ['u',[deriv(f)]]
    if tree[0] == "arctan":
        new_tree = ['/',[deriv(f),['+',[1,['^',[f,2]]]]]]
    if tree[0] == "arcsin":
        new_tree = ['/',[deriv(f),['^',[['-',[1,['^',[f,2]]]],['/',[1,2]]]]]]
    if tree[0] == "arccos":
        new_tree = ['/',[['u',[deriv(f)]],['^',[['-',[1,['^',[f,2]]]],['/',[1,2]]]]]]
    if tree[0] == "log":
        new_tree = deriv(["/",[["ln",[g]],["ln",[f]]]])
    if tree[0] == "exp":
        new_tree = ["*",[["exp",[f]],deriv(f)]]
    return simplify(new_tree)