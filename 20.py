import utils
import math
from collections import defaultdict

def flipv(grid): return list(reversed(grid))
def fliph(grid): return [''.join(list(reversed(row))) for row in grid]
def rot90(grid): return [''.join(l) for l in list(map(list, zip(*grid)))]

def valign(box1, box2):
    return box1[-1] == box2[0] 

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

def fmt(i,n): return '{}_{}'.format(int(i[5:-1]),n)

def build_grids(tiles):
    grids = []

    # Build all versions of each grid
    for title, *grid in tiles:
        grids += [(fmt(title, 'a'),grid), (fmt(title, 'b'),flipv(grid)), (fmt(title, 'c'),fliph(grid)), \
            (fmt(title, 'd'), flipv(fliph(grid))), (fmt(title, 'e'), rot90(grid)), \
            (fmt(title, 'f'), fliph(rot90(grid))), (fmt(title, 'g'), flipv(rot90(grid))), \
            (fmt(title, 'h'), flipv(fliph(rot90(grid))))]

    return grids

def validate(solution, grids, width):
    grids = { title: grid for (title, grid) in grids }
    matrix = utils.chunk(solution, width)
    for y, row in enumerate(matrix):
        for x, col in enumerate(row):
            if x<len(row)-1 and not halign(grids[matrix[y][x]], grids[matrix[y][x+1]]):
                return False
            if x>0 and not halign(grids[matrix[y][x-1]], grids[matrix[y][x]]):
                return False
            if y<len(matrix)-1 and not valign(grids[matrix[y][x]], grids[matrix[y+1][x]]):
                return False
            if y>0 and not valign(grids[matrix[y-1][x]], grids[matrix[y][x]]):
                return False 
    return True

def a(grids, width):
    candidates = defaultdict(set)

    # Build all versions of each grid
    for title, *grid in tiles:
        grids += [(fmt(title, 'a'),grid), (fmt(title, 'b'),flipv(grid)), (fmt(title, 'c'),fliph(grid)), \
            (fmt(title, 'd'), flipv(fliph(grid))), (fmt(title, 'e'), rot90(grid)), \
            (fmt(title, 'f'), fliph(rot90(grid))), (fmt(title, 'g'), flipv(rot90(grid))), \
            (fmt(title, 'h'), flipv(fliph(rot90(grid))))]

    # Find matching pairs
    for i, (idd, grid) in enumerate(grids):
        for idd2, grid2 in grids[i:]:
            if idd[0:4] == idd2[0:4]:
                continue
            if valign(grid, grid2) or halign(grid, grid2) or valign(grid2, grid) or halign(grid2, grid):
                candidates[idd].add(idd2)
                candidates[idd2].add(idd)

    for k, _ in sorted(candidates.items(), key=lambda l: len(l[1])):
        matches = []
        grid = [0 for _ in range(width*width)]
        x,y = 0, 0
        grid[y*width+x] = k
        q = [(grid,k,x,y)]

        visited = set([tuple(grid)])
        while q:
            grid, last, x, y = q.pop(0)
            xx, yy = next(x,y,width)
            if y == width-1 and ((y % 2 == 0 and x == width-1) or (y % 2 == 1 and x == 0)) and validate(grid, grids, width):
                matches.append(grid)

            for c in candidates[last]:

                surr = surrounding(xx,yy,width)
                if all([c in candidates[grid[sy*width+sx]] for (sx,sy) in surr if grid[sy*width+sx] != 0]) and c not in grid:
                    grid = grid[:]
                    grid[yy*width+xx] = c
                    if not tuple(grid) in visited:
                        visited.add(tuple(grid))
                        q.append((grid,c,xx,yy))
                    else:
                        grid[yy*width+xx] = 0
        if matches:
            return matches
    return None

PATTERN = '''                  #
#    ##    ##    ###
 #  #  #  #  #  #'''.split('\n')

def rr(grid): return [l for l in list(map(list, zip(*grid)))]
def flh(grid): return [list(reversed(row)) for row in grid]

def crop(image): return [row[1:-1] for row in image[1:-1]]

def b(grids, ordering, width):
    grid = { title: grid for (title, grid) in grids }
    pp = [row for i, row in enumerate(utils.chunk(ordering, width))]

    joined = [[crop(grid[x]) for x in row] for row in pp] 

    picture = []
    for block0 in joined:
        for i in range(len(block0[0])):
            picture.append(''.join([block[i] for block in block0]))

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
                    matches+=1
                    spacer = ''.join(['+' if n in range(i,i+len(PATTERN[0])+1) else '-' for n in range(len(picture[0]))])
            start += 1
        if matches:
            print(sum([1 for row in picture for c in row if c == '#']) - matches*len(pattern))

tiles = utils.read_input_multi(delim_1='\n\n', delim_2='\n',test=False)
width = int(math.sqrt(len(tiles)))
grids = build_grids(tiles)
result = a(grids, width)[0]

r = [int(rr[0:4]) for rr in result]
print(r[0]*r[width-1]*r[width*width-width]*r[width*width-1])

b(grids, result, width)
