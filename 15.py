
def generate(inp, n):
    spoken, current = { n: i+1 for i, n in enumerate(inp) }, inp[-1]

    for i in range(len(inp), n):
        last = current
        current = i - spoken[last] if last in spoken and spoken[last] != i else 0
        spoken[last] = i
    
    return current

s = "13,16,0,12,15,1"
inp = [int(s) for s in s.split(',')]

print(generate(inp, 2020))
print(generate(inp, 30000000))
