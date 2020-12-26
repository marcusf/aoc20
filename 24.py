import utils
from collections import defaultdict

DELTAS = { 'e': [-1,0], 'ne': [0,-1], 'se':[-1,1],'w':[1,0],'nw': [1,-1],'sw':[0,1]}

def a():
    grid = defaultdict(bool)
    for row in utils.input_lines(test=False):
        curr = (0,0)
        cmd = ''
        for c in row:
            cmd += c
            if cmd in DELTAS:
                curr = (curr[0]+DELTAS[cmd][0], curr[1]+DELTAS[cmd][1])
                cmd = ''
        grid[curr] = not grid[curr]

    print(sum([1 for v in grid.values() if v]))


def neighbors(p):
    return [(p[0]+v[0],p[1]+v[1]) for v in DELTAS.values()]


def b():
    grid = defaultdict(bool)
    for row in utils.input_lines(test=False):
        curr = (0,0)
        cmd = ''
        for c in row:
            cmd += c
            if cmd in DELTAS:
                curr = (curr[0]+DELTAS[cmd][0], curr[1]+DELTAS[cmd][1])
                cmd = ''
        grid[curr] = not grid[curr]
    print(sum([1 for v in grid.values() if v]))
    print('--')

    for round in range(100):
        flip = set()
        for c in list(grid.keys()):
            for adjacent in [c]+neighbors(c):
                colored = len([cc for cc in neighbors(adjacent) if grid[cc]])
                if (grid[adjacent] and (colored == 0 or colored > 2)) or (not grid[adjacent] and colored == 2):
                    flip.add(adjacent)
        
        for f in flip: grid[f] = not grid[f]

        print('Day', round+1,':', sum([1 for v in grid.values() if v]))

b()
