import os
import sys
import numpy as np
from PIL import Image
from collections import defaultdict
from itertools import islice


def input_lines(test=False, generator=str):
    return read_input(delim='\n', generator=generator, test=test)


def read_input(delim=',', fname='', generator=str, test=False):
    if fname == '': fname = os.path.basename(sys.argv[0]).split('.')[0] + ('.test' if test else '.input')

    if delim == None:
        return [generator(i) for i in list(open(fname,'r').read())]
    else:
        return [generator(i) for i in open(fname, 'r').read().split(delim)]

def read_input_multi(delim_1='\n', delim_2=',', fname='', generator=str, test=False):
    if fname == '': fname = os.path.basename(sys.argv[0]).split('.')[0] + ('.test' if test else '.input')
    return [([generator(x) for x in i.split(delim_2)] if delim_2 != None else list(i)) for i in open(fname, 'r').read().split(delim_1)]

def sign(a):
    if a > 0: return 1
    elif a < 0: return -1
    else: return 0

def chunk(list, n):
    return [list[i * n:(i + 1) * n] for i in range((len(list) + n - 1) // n )] 

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


# ===============================================
# An infite list representation from a finite list
class longlist(list):
    def __init__(self, lst):
        self.lst = lst
        self.last_written = 0
        self.spill = defaultdict(int)

    def __setitem__(self, index, value):            
        if index > len(self.lst)-1:
            self.last_written = index
            self.spill[index] = value
        else:
            self.lst[index] = value
        
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.lst[index]
        elif index > len(self.lst)-1:
            return self.spill[index]
        else:
            return self.lst[index]

# ==============================================
# Basic 2D coordinates
class Coord2D:
    def __init__(self, x, y, direction=(1,0)):
        self.x = x
        self.y = y

    def __hash__(self): return hash((self.x, self.y))
    def __str__(self): return f"{self.x}x{self.y}"
    def __repr__(self): return self.__str__()
    def __eq__(self, other): 
        if isinstance(other, tuple): return (self.x, self.y) == other 
        else: return (self.x, self.y) == (other.x, other.y)
    def __ne__(self, other): return not(self == other)
    def __iadd__(self, other): 
        self.x += other.x
        self.y += other.y 
        return self
    def __iter__(self):
        yield self.x
        yield self.y
    def __add__(self, other): 
        if isinstance(other, tuple):
            return Coord2D(self.x+other[0], self.y+other[1])
        else:
            return Coord2D(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Coord2D(self.x-other.x, self.y-other.y)

    def rotate90L(self): # (1,0) becomes (0,-1)
        sx = self.x
        self.x = -self.y
        self.y = sx
        return self
    
    def rotate90R(self): # (1,0) becomes (0,1)
        sx = self.x
        self.x = self.y
        self.y = -sx
        return self

# ==============================================
# Basic 3D coordinates
class Coord3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self): return hash((self.x, self.y, self.z))
    def __str__(self): return f"{self.x}x{self.y}x{self.z}"
    def __repr__(self): return self.__str__()
    def __eq__(self, other): 
        if isinstance(other, tuple): return (self.x, self.y, self.z) == other 
        else: return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    def __ne__(self, other): return not(self == other)
    def __iadd__(self, other): 
        self.x += other.x
        self.y += other.y 
        self.z += other.z
        return self
    def __sub__(self, other):
        return Coord3D(self.x-other.x, self.y-other.y, self.z-other.z)

# ===================================================
# Simple grid layer. Combine with other grid layers
# to get a grid that can compute intersections.
# Each point can have a value and a meta-value, which
# is just a place to shove shit that might be needed.
class GridLayer:

    def __init__(self, value_constructor=int, meta_constructor=int):
        self.grid = defaultdict(value_constructor)
        self.meta = defaultdict(meta_constructor)
        self.value_constructor = value_constructor
        self.grid_bag = set()
        self.minx = sys.maxsize
        self.miny = sys.maxsize
        self.maxx = -sys.maxsize
        self.maxy = -sys.maxsize

    def __iter__(self):
        return iter(self.grid.items())

    def __getitem__(self, key):
        if isinstance(key, Coord2D):
            x, y = key.x, key.y
        else:
            x, y = key
        return self.get(x, y)

    def __setitem__(self, key, val):
        if isinstance(key, Coord2D):
            x, y = key.x, key.y
        else:
            x, y = key
        self.put(x, y, val)

    def bounds(self):
        return (self.minx, self.miny, self.maxx, self.maxy)

    def inside(self, p):
        return p.x >= self.minx and p.x <= self.maxx and p.y >= self.miny and p.y <= self.maxy

    def put(self, x, y, val):
        self.grid[Coord2D(x,y)] = val
        self.grid_bag.add(Coord2D(x,y))
        self.minx = min(x, self.minx)
        self.miny = min(y, self.miny)
        self.maxx = max(x, self.maxx)
        self.maxy = max(y, self.maxy)
    
    def get(self, x, y):
        return self.grid[Coord2D(x,y)]

    def adjacent(self, pos):
        g = self.grid.copy()
        return [
            (pos+(1,0), g[pos+(1,0)], self.meta[pos+(1,0)]),
            (pos+(-1,0), g[pos+(-1,0)], self.meta[pos+(-1,0)]),
            (pos+(0,1), g[pos+(0,1)], self.meta[pos+(0,1)]),
            (pos+(0,-1), g[pos+(0,-1)], self.meta[pos+(0,-1)]),
        ]

    def wide_adjacent(self, pos):
        g = self.grid.copy()
        return [
            (pos+(1,0), g[pos+(1,0)], self.meta[pos+(1,0)]),
            (pos+(-1,0), g[pos+(-1,0)], self.meta[pos+(-1,0)]),
            (pos+(0,1), g[pos+(0,1)], self.meta[pos+(0,1)]),
            (pos+(0,-1), g[pos+(0,-1)], self.meta[pos+(0,-1)]),

            (pos+(-1,-1), g[pos+(-1,-1)], self.meta[pos+(-1,-1)]),
            (pos+(1,1), g[pos+(1,1)], self.meta[pos+(1,1)]),
            (pos+(1,-1), g[pos+(1,-1)], self.meta[pos+(1,-1)]),
            (pos+(-1,1), g[pos+(-1,1)], self.meta[pos+(-1,1)])
        ]

    def put_meta(self, x, y, v=None):
        if v == None:
            self.meta[x] = y
        else:
            self.meta[Coord2D(x,y)] = v

    def connected_graph(self, exclude={}):
        connected, bag = {}, set()
        for k in self.grid_bag:
            if not self.grid[k] in exclude:
                bag.add(k)
                adjacents = self.adjacent(k)
                connected[k] = [a[0] for a in adjacents if a[0] in self.grid_bag and not self.grid[a[0]] in exclude]
        return bag, connected

    def bfs(self, start, end, exclude={}):
        q = [(start,[start])]
        visited = set()
        nodes, edges = self.connected_graph(exclude)
        while q:
            v, g = q.pop(0)
            if v == end:
                return v,g
            else:
                for edge in edges[v]:
                    if not edge in visited:
                        visited.add(edge)
                        q.append((edge, g+[edge]))

    def get_meta(self, x_or_coord, y=None):
        if y == None:
            return self.meta[x_or_coord]
        else:
            return self.meta[Coord2D(x_or_coord,y)]

    def putif_meta(self, x, y, guard, val):
        if self.get_meta(x,y) == guard:
            self.put_meta(x,y,val)

    def print(self, factory=None):
        _int_printer = lambda c: '#' if c == 1 else ' '
        _str_printer = lambda c: c if c else ' '
        if factory == None:
            if self.value_constructor == int:
                factory = _int_printer
            else:
                factory = _str_printer
        
        minx, miny, maxx, maxy = self.bounds()
        print(''.join(['-' for _ in range(minx, maxx+1)]))
        for y in range(miny, maxy+1):
            l = []
            for x in range(minx, maxx+1):
                l.append(factory(self[(x,y)]))
            print(''.join(l)) 
        print(''.join(['-' for _ in range(minx, maxx+1)]))

# ========================================
# A combination of many GridLayer's
class Grid:

    def __init__(self, value_constructor=int, meta_constructor=int):
        self.layers = []
        self.value_constructor=value_constructor
        self.meta_constructor=meta_constructor

    def add_layer(self):
        layer = GridLayer(self.value_constructor, self.meta_constructor)
        self.layers.append(layer)
        return layer

    def intersection(self):
        return set.intersection(*[s.grid_bag for s in self.layers])

    def bounds(self):
        b = list(self.layers[0].bounds())
        for l in self.layers:
            nb = l.bounds()
            if nb[0] < b[0]: b[0] = nb[0]
            if nb[1] < b[1]: b[1] = nb[1]
            if nb[2] > b[2]: b[2] = nb[2]
            if nb[3] > b[3]: b[3] = nb[3]
        return tuple(b)

    # Uses numpy to output an image. Usually more helpful than text 
    # for larger grids. Varies colors.
    def pretty_image(self):
        bounds = self.bounds()
        width = bounds[2]-bounds[0]
        height = bounds[3]-bounds[1]
        off_x, off_y = -bounds[0], -bounds[1]
        print(width, height)
        array = np.full((height+1,width+1,3), 255, dtype=np.uint8)
        
        for i, l in enumerate(self.layers):
            r = 200 if (i+2) % 2 == 0 else 0
            g = 200 if (i+2) % 3 == 0 else 0
            b = 200 if (i+2) % 4 == 0 else 0
            for cord in l.grid_bag:
                array[cord.y+off_y][cord.x+off_x] = [r,g,b]
        return Image.fromarray(array).show()

class Graph:

    def __init__(self):
        self.edges = defaultdict(set)
        self.weights = defaultdict(int)
        self.nodes = set()
        self.back = defaultdict(set)

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, frm, to, weight):
        self.edges[frm].add(to)
        self.back[to].add(frm)
        self.weights[(frm,to)] = weight

