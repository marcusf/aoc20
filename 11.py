import utils

def adjacent(graph, point):
    return (
        first_hit(graph, point,  0,  1),
        first_hit(graph, point,  0, -1),
        first_hit(graph, point,  1,  0),
        first_hit(graph, point, -1,  0),
        first_hit(graph, point,  1,  1),
        first_hit(graph, point, -1,  1),
        first_hit(graph, point, -1, -1),
        first_hit(graph, point,  1, -1)
    )

def first_hit(graph, point, dx, dy):
    p = utils.Coord2D(point.x,point.y)
    while True:
        p.x += dx
        p.y += dy
        if not graph.inside(p):
            break
        if graph[p] != '.':
            return graph[p]
    return '.'

def find(grid, adjacency, treshhold):
    while True:
        actions = []
        for coord, val in grid:
            if val == '.':
                continue
            adjacent = len([c for (_, c, __) in adjacency(grid, coord) if c == '#'])
            if val == 'L' and adjacent == 0:
                actions.append((coord, '#'))
            elif val == '#' and adjacent >= treshhold:
                actions.append((coord, 'L'))
        if len(actions) == 0:
            print(len([val for _, val in grid if val == '#']))
            break
        else:
            [grid.put(c.x,c.y,v) for (c,v) in actions]

def a(grid):
    find(grid, lambda grid, coord: grid.wide_adjacent(coord), 4)
    # while True:
    #     actions = []
    #     for coord, val in grid:
    #         if val == '.':
    #             continue
    #         adjacent = len([c for (_, c, __) in grid.wide_adjacent(coord) if c == '#'])
    #         if val == 'L' and adjacent == 0:
    #             actions.append((coord, '#'))
    #         elif val == '#' and adjacent >= 4:
    #             actions.append((coord, 'L'))
    #     if len(actions) == 0:
    #         print(len([val for _, val in grid if val == '#']))
    #         break
    #     else:
    #         [grid.put(c.x,c.y,v) for (c,v) in actions]

def b(grid):
    while True:
        actions = []
        for coord, val in grid:
            if val == '.':
                continue
            adj = len([c for c in adjacent(grid, coord) if c == '#'])
            if val == 'L' and adj == 0:
                actions.append((coord, '#'))
            elif val == '#' and adj >= 5:
                actions.append((coord, 'L'))
        if len(actions) == 0:
            print(len([val for _, val in grid if val == '#']))
            break
        else:
            [grid.put(c.x,c.y,v) for (c,v) in actions]



input = utils.input_lines(test=False)
grid = utils.GridLayer(value_constructor=str)
[grid.put(x,y,c) for y, line in enumerate(input) for x, c in enumerate(line)]

a(grid)
b(grid)