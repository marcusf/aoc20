import utils
import math
from collections import defaultdict
import functools

def flipv(grid): return list(reversed(grid))
def fliph(grid): return [''.join(list(reversed(row))) for row in grid]
def rot90(grid): return [''.join(l) for l in list(map(list, zip(*grid)))]
def crop(grid): return [row[1:-1] for row in grid[1:-1]]

def fmt(i,n): return '{}:{}'.format(int(i[5:-1]),n)
def row(title, operation, grid):
    # To avoid costly compares in connected_grid,
    # we hash each of the edges and compare the hashes.
    t = fmt(title, operation)
    return (t, grid, int(t[0:4]), hash_grid(grid))

def build_grids(tiles):
    grids = []
    for title, *grid in tiles:
        grids += [row(title, 'normal', grid),\
                 row(title, 'flipv', flipv(grid)),\
                 row(title, 'fliph', fliph(grid)),\
                 row(title, 'flipv:fliph', flipv(fliph(grid))),\
                 row(title, 'rot90', rot90(grid)),\
                 row(title, 'fliph:rot90', fliph(rot90(grid))),\
                 row(title, 'flipv:rot90', flipv(rot90(grid)))]
    return grids

def hash_grid(g):
    rg = rot90(g)
    return [hash(''.join(gr)) for gr in [g[0], g[-1], rg[0], rg[-1]]]

def valign(box1, box2):
    return box1[-1] == box2[0]

def halign(box1, box2):
    for i in range(len(box1)):
        if not box1[i][-1] == box2[i][0]:
            return False
    return True

def connected(label1, hash1, label2, hash2):
    return (label1 != label2) and (hash1[0] == hash2[1] or hash1[1] == hash2[0] \
        or hash1[2] == hash2[3] or hash1[3] == hash2[2])

def connect(list, a1, a2):
    list[a1].append(a2)
    list[a2].append(a1)

def connected_grids(grids):
    candidates = defaultdict(list)
    [connect(candidates,k1,k2) for i, (k1, _, l1, h1) in enumerate(grids) for k2, _, l2, h2 in grids[i:] if connected(l1, h1, l2, h2)]
    return candidates

def is_complete(x,y,w):
    return y == w-1 and ((y % 2 == 0 and x == w-1) or (y % 2 == 1 and x == 0))

def aligns(g1,x1,y1,g2,x2,y2):
    if x1 == x2: return valign(g1,g2) if y1 < y2 else valign(g2,g1)
    if y1 == y2: return halign(g1,g2) if x1 < x2 else halign(g2,g1)

def next(x,y,w):
    if (x == w-1 and y % 2 == 0) or (x == 0 and y % 2 == 1):
        y += 1
        x = -1 if y % 2 == 0 else w
    x = x + 1 if y % 2 == 0 else x - 1
    return (x,y)

def dfs(start, grids, candidates, width):
    grid = [0 for _ in range(width**2)]

    grid[0] = start
    q = [(grid,start,0,0)]

    visited = set()

    while q:
        grid, last, x, y = q.pop()
        
        if is_complete(x, y, width): return grid
        if tuple(grid) in visited: continue
        visited.add(tuple(grid))

        xx, yy = next(x,y,width)
        for c in candidates[last]:
            if c not in grid and aligns(grids[last],x,y,grids[c],xx,yy):
                grid = grid[:]
                grid[yy*width+xx] = c
                q.append((grid,c,xx,yy))

    return None

def make_pictures(grids, ordering, width):
    grid = { title: grid for (title, grid, _, _) in grids }
    pp = [row for i, row in enumerate(utils.chunk(ordering, width))]
    joined = [[crop(grid[x]) for x in row] for row in pp] 

    picture = []
    for blocks in joined:
        for i in range(len(blocks[0])):
            picture.append(''.join([block[i] for block in blocks]))

    return [flipv(fliph(rot90(picture))), flipv(picture), fliph(picture), \
            flipv(fliph(picture)), rot90(picture),\
            fliph(rot90(picture)), flipv(rot90(picture)),picture]

def make_pattern():
    PATTERN = '''                  #
#    ##    ##    ###
 #  #  #  #  #  #'''.split('\n')
    pattern = { (y,x) for y, row in enumerate(PATTERN) for x, col in enumerate(row) if col == '#' }
    pw = len(PATTERN[0])+1
    return pattern, pw

def scan_one(r0,r1,r2,pattern,width):
    matches = 0
    for i in range(0, len(r0)-width):
        candidate = [r0[i:i+width], r1[i:i+width], r2[i:i+width]]
        found = True
        for y,x in pattern:
            if not candidate[y][x] == '#':
                found = False
        if found:
            matches+=1
    return matches

def a(grids, width):
    graph = connected_grids(grids)
    tiles = { title: grid for (title, grid, _, _) in grids }
    corners = [k for k, v in graph.items() if len(v) == 2]

    for corner in corners:
        r = dfs(corner, tiles, graph, width)
        if r: 
            ints = [int(rr[0:4]) for rr in r]
            return r, ints[0]*ints[width-1]*ints[width**2-width]*ints[width**2-1]

    return None

def b(grids, ordering, pic_width):
    pictures = make_pictures(grids, ordering, pic_width)
    pattern, width = make_pattern()

    for picture in pictures:
        matches = sum([scan_one(r0,r1,r2,pattern,width) for r0,r1,r2 in utils.window(picture, 3)])
        if matches:
            return sum([1 for row in picture for c in row if c == '#']) - matches*len(pattern)

def main():
    tiles = utils.read_input_multi(delim_1='\n\n', delim_2='\n',test=False)
    width = int(math.sqrt(len(tiles)))
    grids = build_grids(tiles)

    pattern, a_res = a(grids, width)
    b_res = b(grids, pattern, width)

    print(a_res, a_res == 17148689442341)
    print(b_res, b_res == 2009)

main()