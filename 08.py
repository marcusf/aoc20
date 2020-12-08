import utils

code = [[a,int(b),False] for [a,b] in utils.read_input_multi(delim_2=' ')]

def run(code):
    ptr, acc = 0, 0
    while True:
        if ptr >= len(code):
            return acc, True
        row = code[ptr]
        instr, val, visited = row
        if visited:
            return acc, False
        row[2] = True
        if instr == 'jmp':
            ptr += val
        elif instr == 'nop':
            ptr += 1
        elif instr == 'acc':
            acc += val
            ptr += 1

print(run(code)[0])

for i in range(len(code)):
    c = [[op, val, False] for [op, val, _] in code]
    if c[i][0] == 'acc':
        continue
    c[i][0] = 'nop' if c[i][0] == 'acc' else 'nop'
    result, finished = run(c)
    if finished:
        print(result)
        break    
