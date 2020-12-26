import utils
import math
from collections import defaultdict

def flipv(grid): return list(reversed(grid))
def fliph(grid): return [''.join(list(reversed(row))) for row in grid]
def rot90(grid): return [''.join(l) for l in list(map(list, zip(*grid)))]

def valign(box1, box2):
    return box1[0] == box2[-1] 

def halign(box1, box2):
    return [b[-1] for b in box1] == [b[0] for b in box2]

def surrounding(x,y,w):
    return [(x,y) for x,y in [(x+1, y), (x-1,y), (x,y+1),(x,y-1)] if x>=0 and x<w and y>=0 and y<w]

def next(x,y,w):
    if (x == w-1 and y % 2 == 0) or (x == 0 and y % 2 == 1):
        y = y+1
        x = -1 if y % 2 == 0 else w
    if y % 2 == 0:
        x += 1
    else:
        x -= 1
    return (x,y)

def a(tiles, width):
    grids, candidates = {}, defaultdict(set)

    # Build all versions of each grid
    for title, *grid in tiles:
        grids[int(title[5:-1])] = [grid, flipv(grid), fliph(grid), flipv(fliph(grid)), rot90(grid), \
            fliph(rot90(grid)), flipv(rot90(grid)), flipv(fliph(rot90(grid)))]

    # Find matching pairs
    for idd, grid in grids.items():
        for idd2, grid2 in grids.items():
            if idd == idd2:
                continue
            for g1 in grid:
                for g2 in grid2:
                    if valign(g1,g2):
                        candidates[idd].add(idd2)

    # For each item, do a BFS to see if we can fill out the grid.
    # First result, finish up.
    for k in candidates.keys():
        grid = [0 for _ in range(width*width)]
        x,y = 0, 0
        grid[y*width+x] = k
        q = [(grid,k,x,y)]

        visited = set([tuple(grid)])
        while q:
            grid, last, x, y = q.pop(0)
            xx, yy = next(x,y,width)
            if y == width-1 and ((y % 2 == 0 and x == width-1) or (y % 2 == 1 and x == 0)):
                return grid

            for c in candidates[last]:
                surr = surrounding(xx,yy,width)
                if all([c in candidates[grid[sy*width+sx]] for (sx,sy) in surr if grid[sy*width+sx] != 0]) and c not in grid:
                    grid = grid[:]
                    grid[yy*width+xx] = c
                    if not tuple(grid) in visited:
                        visited.add(tuple(grid))
                        q.append((grid,c,xx,yy))


tiles = utils.read_input_multi(delim_1='\n\n', delim_2='\n',test=True)
width = int(math.sqrt(len(tiles)))
# result = a(tiles, width)
# print(result[0]*result[width-1]*result[width*width-width]*result[width*width-1])

# just because my solver takes 1 million years, we'll do this.
# n.b. the result comes like a snake.
# 1 2 3
# 6 5 4
# 7 8 9
reslt = [3181, 2609, 2297, 3739, 1277, 3167, 2531, 2393, 2243, 1549, 3659, 1453, 1571, 1987, 2803,\
          3767, 3109, 1289, 1231, 2269, 2309, 3637, 1993, 2969, 3833, 2447, 2647, 2903, 2549, 1483,\
          3541, 1447, 1889, 3779, 1193, 2137, 3943, 1627, 2383, 2791, 3361, 3011, 3119, 2441, 1951,\
          3203, 1051, 1531, 2203, 1613, 3881, 1601, 2207, 3001, 1321, 2503, 2707, 2027, 3733, 1481,\
          2579, 2699, 3169, 1609, 1499, 1867, 3023, 3083, 3061, 3359, 2053, 2879, 1061, 1283, 2687,\
          2161, 1229, 1999, 2861, 3343, 2551, 2273, 1307, 2837, 1361, 2957, 3041, 1439, 1621, 2473,\
          1741, 2389, 1471, 3433, 2851, 2719, 3163, 1913, 3863, 2819, 2399, 1151, 1489, 1733, 2939,\
          1861, 2731, 2693, 1871, 3391, 2089, 2971, 2437, 3623, 3389, 3559, 3407, 2423, 2111, 3823,\
          2909, 1097, 1669, 2213, 3067, 2953, 3347, 1213, 2069, 1559, 1543, 1699, 2543, 3847, 3037,\
         3499, 3533, 2333, 3719, 1291, 3121, 1009, 1019, 1459]

result = a(tiles, width)
print(result)

PATTERN = '''                  #
#    ##    ##    ###
 #  #  #  #  #  #'''.split('\n')

def b(tiles, ordering, width):
    grid = { int(title[5:-1]): grid for title, *grid in tiles }
    pp = [row for i, row in enumerate(utils.chunk(ordering, width))]
    print(pp)
    print([l for l in list(map(list, zip(*pp)))])
    joined = [row for i, row in enumerate(utils.chunk([grid[o] for o in ordering], width))]

    picture = []
    
    for block0 in joined:
        for i in range(len(block0[0])):
            picture.append(''.join([block[i] for block in block0]))

    [print(p) for p in picture]

    pattern = { (y,x) for y, row in enumerate(PATTERN) for x, col in enumerate(row) if col == '#' }
    pw = len(PATTERN[0])+1

    pictures = [picture, flipv(picture), fliph(picture), flipv(fliph(picture)), rot90(picture), \
            fliph(rot90(picture)), flipv(rot90(picture)), flipv(fliph(rot90(picture)))]
    
    
    for qq, picture in enumerate(pictures):
        matches = 0
        start = 0
        for r0,r1,r2 in utils.window(picture, 3):
            for i in range(0, len(r0)-pw):
                candidate = [r0[i:i+pw], r1[i:i+pw], r2[i:i+pw]]
                found = True
                for y,x in pattern:
                    if not candidate[y][x] == '#':
                        found = False
                if found:
                    print(start,i)
                    matches+=1
                    spacer = ''.join(['+' if n in range(i,i+len(PATTERN[0])+1) else '-' for n in range(len(picture[0]))])
                    [print(spacer+'\n'+row if n in [start,start+3] else row) for n,row in enumerate(picture)]
                    print(qq, 'hojtarolja')
            start += 1
        if matches:
            # too big 4992.
            print(sum([1 for row in picture for c in row if c == '#']) - matches*len(pattern))







b(tiles, result, width)


