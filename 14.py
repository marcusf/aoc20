import utils
import re

def a(program):
    mask1s, mask0s = 0,0
    data = dict()

    for row in program:
        if row[0:4] == 'mask':
            mask = row[7:]
            mask1s = int(mask.replace('X','0'), 2)
            mask0s = int(mask.replace('X','1'), 2)
        else:
            # mem[8] = 11
            loc, num = [int(i) for i in re.match(r'mem\[(\d+)\] = (\d+)', row).groups()]
            data[loc] = (num | mask1s) & mask0s

    print(sum(data.values()))

def explode(pattern):
    lst = []
    q = [[pattern, '']]
    while q:
        input, output = q.pop(0)
        if len(input) == 0:
            lst.append(int(output,2))
        else:
            if input[0] == 'X':
                q.append([input[1:], output+'1'])
                q.append([input[1:], output+'0'])
            else:
                q.append([input[1:], output+input[0]])
    return lst

def interleave(mask, n):
    s = format(n, '036b')
    l = []
    for i in range(36):
        if mask[i] == 'X':
            l.append('X')
        if mask[i] == '1':
            l.append('1')
        if mask[i] == '0':
            l.append(s[i])
    return "".join(l)

def b(program):
    data = dict()
    mask = ''

    for row in program:
        if row[0:4] == 'mask':
            mask = row[7:]
        else: 
            loc, num = [int(i) for i in re.match(r'mem\[(\d+)\] = (\d+)', row).groups()]
            adresses = [] 
            inp = interleave(mask, loc)
            adresses = explode(inp)
            for a in adresses:
                data[a] = num
    
    print(sum(data.values()))

program = utils.input_lines(test=False)

a(program)
b(program)
