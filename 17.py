from utils import *

start = input_lines(test=False)

def a(start):
    space = Space3D()

    for y, row in enumerate(start):
        for x, col in enumerate(row):
            if col == '#':
                space.add(Coord3D(x-1, y-1, 0))

    for _ in range(6):
        newspace = Space3D()
        for cube, _ in space.universe():
            for p in cube.adjacent():
                neighbors = len([1 for pp in p.adjacent() if pp in space])
                active = p in space
                if (active and neighbors in [2,3]) or (not active and neighbors == 3):
                    newspace.add(p)
        space = newspace

    print(len(space.points))

def b(start):
    space = Space4D()

    for y, row in enumerate(start):
        for x, col in enumerate(row):
            if col == '#':
                space.add(Coord4D(x-1, y-1, 0, 0))

    for _ in range(6):
        newspace = Space4D()
        for cube, _ in space.universe():
            for p in cube.adjacent():
                neighbors = len([1 for pp in p.adjacent() if pp in space])
                active = p in space
                if (active and neighbors in [2,3]) or (not active and neighbors == 3):
                    newspace.add(p)
        space = newspace

    print(len(space.points))

b(start)