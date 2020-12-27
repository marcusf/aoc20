class Clock:

    def __init__(self, seed, maxx):
        lst = seed[:]
        self.clock = {}
        lst += list(range(max(lst)+1, maxx+1))
        for i, v in enumerate(lst):
            if i+1 < len(lst):
                self.clock[v] = lst[i+1]
        self.clock[lst[-1]] = lst[0]
        self.current = lst[0]
        self.max = maxx
        self.min = 1

    def pick_up(self):
        return ([self.clock[self.current], \
        self.clock[self.clock[self.current]], \
        self.clock[self.clock[self.clock[self.current]]]], self.current)

    def get_destination(self, avoid=[]):
        destination_value = self.current-1
        if destination_value < self.min:
            destination_value = self.max

        while destination_value in avoid:
            destination_value -= 1
            if destination_value < self.min:
                destination_value = self.max
            
        return destination_value

    def move(self, idx, values, destination):
        nxt = self.clock[values[-1]]
        self.clock[idx] = nxt
        
        nxt = self.clock[destination]
        self.clock[destination] = values[0]
        self.clock[values[-1]] = nxt
    
    def increment_current(self):
        self.current = self.clock[self.current]

    def print_win(self):
        a = self.clock[1]
        b = self.clock[a]
        print(a*b)

input = '326519478'

def b(input):
    clock = Clock([int(a) for a in input], 1_000_000)
    for _ in range(10_000_000):
        to_move, idx = clock.pick_up()
        destination = clock.get_destination(avoid=to_move)
        clock.move(idx, to_move, destination)
        clock.increment_current()
    clock.print_win()

def a(input):
    clock = Clock([int(a) for a in input], len(input))
    for _ in range(100):
        to_move, idx = clock.pick_up()
        destination = clock.get_destination(avoid=to_move)
        clock.move(idx, to_move, destination)
        clock.increment_current()
    result, nxt = '', clock.clock[1]
    while True:
        result += str(nxt)
        nxt = clock.clock[nxt]
        if nxt == 1:
            break
    print(''.join(result))

a(input)
b(input)
