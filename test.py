import utils

a = utils.GridLayer()
a.put(0,0,0)
a.put(0,1,0)
a.put(0,2,0)
a.put(1,0,1)
a.put(1,1,0)
a.put(1,2,1)
a.print()
print(a.connected_graph(exclude=set([1])))
print(a.bfs(utils.Coord2D(0,0), utils.Coord2D(1,1)))