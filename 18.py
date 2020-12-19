import utils
import re

def a(input,i=0):
    nums, op = [], None
    while i < len(input):
        c = input[i]
        if c == " ": 
            i+=1
            continue
        elif c == "+":
            i+=1
            op = lambda a,b: a+b
        elif c == "*":
            i+=1
            op = lambda a,b: a*b
        elif c == "(":
            i,nm=a(input,i+1)
            nums.append(nm)
        elif c == ")":
            return i+1, nums[0]
        else: 
            i += 1
            nums.append(int(c))

        if len(nums) == 2:
            nums.append(op(nums.pop(),nums.pop()))
    return nums[0]

# Simplified this from http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html
# after recalling RPN from college
def shunting_yard(expression):
    values, operators = [], []
    for token in expression:
        if token == ' ':
            continue
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = operators[-1] 
            while top is not None and top != '(':
                values.append(eval("{0}{1}{2}".format(values.pop(), operators.pop(), values.pop())))
                top = operators[-1] 
            operators.pop() # Discard the '('
        elif token in ['+','*']:
            top = operators[-1] if operators else None
            while top is not None and top == '+':
                values.append(eval("{0}{1}{2}".format(values.pop(), operators.pop(), values.pop())))
                top = operators[-1] if operators else None
            operators.append(token)
        else:
            values.append(int(token))

    while operators:
        values.append(eval("{0}{1}{2}".format(values.pop(), operators.pop(), values.pop())))
 
    return values[0]


rows = utils.input_lines()
print(sum([a(row) for row in utils.input_lines()]))
print(sum([shunting_yard(row) for row in utils.input_lines()]))
