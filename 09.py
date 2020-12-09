import utils

input = utils.read_input(delim='\n', generator=int)

def a(input):
    for i in range(25,len(input)):
        num = input[i]
        seeds = input[i-25:i]
        found = False
        for x in range(0, len(seeds)):
            for y in range(0, len(seeds)):
                if num == seeds[x]+seeds[y]:
                    found = True
                    break
        if not found:
            print(num)
            return num


def b(inp, num):
    lo, hi, val = 0, 1, inp[0]+inp[1]
    while True:
        if val == num:
            rang = inp[lo:hi+1]
            return max(rang)+min(rang)
        elif val < num:
            hi+=1
            val += inp[hi]
        else:
            val -= inp[lo]
            lo+=1

num = a(input)
print(b(input, num))