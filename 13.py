import utils
from functools import reduce

# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
input = utils.input_lines()
departure, buses = int(input[0]), [(t, int(x)) for t, x in enumerate(input[1].split(',')) if x != 'x']

mini = sorted([(bus*(1+departure//bus)-departure,bus) for t, bus in buses])[0]
print(mini[0]*mini[1])
times, primes = list(zip(*buses))
times = [-t for t in times]

print(chinese_remainder(primes, times))