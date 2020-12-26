import re
import math

card_pk = 8335663
door_pk = 8614349

modulo = 20201227

def algo(subject_number, loop_size):
    val = 1
    for _ in range(loop_size):
        val = subject_number*val % modulo
    return val

# I am sure there is a much more elegant way to do this, but this worked.
# via SO.
def baby_steps_giant_steps(a,b,p):
    N = 1 + int(math.sqrt(p))

    #initialize baby_steps table
    baby_steps = {}
    baby_step = 1
    for r in range(N+1):
        baby_steps[baby_step] = r
        baby_step = baby_step * a % p

    #now take the giant steps
    giant_stride = pow(a,(p-2)*N,p)
    giant_step = b
    for q in range(N+1):
        if giant_step in baby_steps:
            return q*N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % p
    return -1

card_ls = baby_steps_giant_steps(7, card_pk, modulo)
door_ls = baby_steps_giant_steps(7, door_pk, modulo)


print(algo(card_pk, door_ls))

