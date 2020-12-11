import utils
import numpy as np
from PIL import Image

input = utils.read_input(delim='\n', generator=int)

def a(input):
    for i in range(25,len(input)):
        num = input[i]
        seeds = input[i-25:i]
        found = False
        for x in range(0, len(seeds)):
            for y in range(x, len(seeds)):
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

def draw_b(inp, num):
    lo, hi, val = 0, 1, inp[0]+inp[1]
    lst = []
    while True:
        if val == num:
            rang = inp[lo:hi+1]
            return lst
        elif val < num:
            hi+=1
            val += inp[hi]
        else:
            val -= inp[lo]
            lo+=1
        lst.append((lo, hi))


num = a(input)

l = draw_b(input, num)
width, height = len(input)+10, len(l)
array = np.full((height, width, 3), 255, dtype=np.uint8)
for y, (lo, hi) in enumerate(l):
    array[y][lo+10] = [0,0,255]
    array[y][hi+10] = [255,0,0]
Image.fromarray(array).show()
