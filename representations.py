#Representations file to provide conversions from infix -> RPN ->
#tree.

from tokens import *

#Use shunting yard algorithm to convert infix -> RPN
def shunting_yard(infix_string): # Still need to write this
    pass

#Convert RPN -> tree via pushing and popping
def rpn_to_tree(array):
    stack = []
    for x in array:
        if x in binary_operator_tokens:
            a = stack.pop()
            b = stack.pop()
            stack.append([x,[b,a]]) #Watch the order!
        elif x in unary_operator_tokens:
            a = stack.pop()
            stack.append([x,[a]])
        else:
            stack.append(x)
    return stack[0]

#Next function converts tree -> infix expression

#General logic here: the non-inline operators are easy.  for example,
    # sin(2) is represented by the tree ["sin",[2]], so this
    # conversion is easy.

#Inline operators cause all the trouble, owing to needing to know
    #where to put parentheses.  Rules: if the operator higher on the
    #tree has higher precedence, throw parentheses in.  Also need
    #parentheses around if (a) have the same precedence,
    #(b) higher operation is non-associative, and (c) the operand
    #is on the "wrong" side.

#Regarding this last condition, we compute + and - left to right.
    #Therefore, for the RPN 4 5 6 + -, we need parentheses around the
    #5+6, as the right-operand in a left-to-right evaluation.

#Special case: when exponentiating a non-inline function, put
    #parenthesis around it.
def tree_to_string(tree):
    if type(tree) in number_types or tree in variable_tokens:
        return str(tree)
    x = tree[0]

    if x in inline_operators:
        beginning = tree_to_string(tree[1][0])
        end = tree_to_string(tree[1][1])
        if type(tree[1][0]) == list:
            if tree[1][0][0] in inline_operators:
                upper_precedence = binary_operations_data[x][1]
                lower_precedence = binary_operations_data[tree[1][0][0]][1]
                if upper_precedence > lower_precedence or (upper_precedence == lower_precedence and binary_operations_data[x][0] == "right" and binary_operations_data[x][2] == 0):
                    beginning = "(" + beginning + ")"
            if x == "^" and tree[1][0][0] not in inline_operators:
                beginning = "(" + beginning + ")"
        if type(tree[1][1]) == list:
            if tree[1][1][0] in inline_operators:
                upper_precedence = binary_operations_data[x][1]
                lower_precedence = binary_operations_data[tree[1][1][0]][1]
                if upper_precedence > lower_precedence or (upper_precedence == lower_precedence and binary_operations_data[x][0] == "left" and binary_operations_data[x][2] == 0):
                    end = "(" + end + ")"
        return beginning + x + end
    elif x == "log":
        return x + "(" + tree_to_string(tree[1][0]) + "," + tree_to_string(tree[1][1]) + ")"
    elif x == "u":
        return "(-" + tree_to_string(tree[1][0]) + ")"
    else:
        return x + "(" + tree_to_string(tree[1][0]) + ")"
