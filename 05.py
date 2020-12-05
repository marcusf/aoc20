import math
import utils

def bsp(instr, lo, hi, max):
    low, high = 0, max
    for c in instr:
        cut = math.floor((high-low)/2)
        if c == lo:
            high -= cut
        elif c == hi:
            low += cut
    return low

def get_seat(code):
    row = bsp(code[:-3],"F","B",128)
    col = bsp(code[-3:],"L","R",8)
    return row*8+col

seats = [get_seat(pazz) for pazz in utils.read_input(generator=str, delim='\n')]

print(max(seats)) # A
print([lo+1 for lo, mid, _ in utils.window(sorted(seats),3) if lo+1 != mid][0]) # B
