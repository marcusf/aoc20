input = '326519478'

clock = [int(a) for a in input]
clock = clock + list(range(10, 1_000_001))
def a(input):
    clock = [int(a) for a in input]
    for i in range(100):
        pickup = clock[1:4]
        destval = clock[0]-1
        destination = clock.index(destval if destval >= 1 else 9)
        i = 1
        while destination in [1,2,3]:
            destval = destval - i
            if destval < 1: # min(clock):
                destval = 9 # max(clock)
            destination = clock.index(destval)
        clock[destination+1:1] = pickup 
        del clock[1]
        del clock[1]
        del clock[1]
        a = clock.pop(0)
        clock.append(a)

    start = clock.index(1)
    result = ''.join([str(s) for s in clock[start+1:] + clock[0:start]])
    print(result)

def b(input):
    has_seen = set()
    clock = [int(a) for a in input]
    clock = clock + list(range(10, 1000))
    for i in range(100000):
        print(i, clock)
        strt = clock.index(1)

        if i % 1000 == 0:
            print(i)

        pickup = clock[1:4]
        destval = clock[0]-1
        destination = clock.index(destval if destval >= 1 else 9)
        i = 1
        while destination in [1,2,3]:
            destval = destval - i
            if destval < 1: # min(clock):
                destval = 9 # max(clock)
            destination = clock.index(destval)
        clock[destination+1:1] = pickup 
        del clock[1]
        del clock[1]
        del clock[1]
        a = clock.pop(0)
        clock.append(a)

    start = clock.index(1)
    print(clock[(start+2)%len(clock)], clock[(start+2)%len(clock)])
    print(clock[start+1]*clock[start+2])

b(input)
