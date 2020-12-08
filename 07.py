import utils
import re
from collections import defaultdict

input = utils.input_lines(test=False)
graph = utils.Graph()

for row in input:
    g, *gs = re.match(r'([a-zA-Z\s]+) contain (.*)', row).groups()
    graph.add_node(g)
    if gs[0] == 'no other bags.': continue
    else:
        gs = gs[0][:-1].split(', ')
    for line in gs:
        count, bag = int(line[0]), line[2:]
        if bag[-1] != 's': 
            bag = bag + 's'
        graph.add_edge(g, bag, count)

# Part 1
q = ['shiny gold bags']
score = 0
visited = set()
while len(q):
    node = q.pop(0)
    for g in graph.back[node]:
        if not g in visited:
            q.append(g)
            visited.add(g)


print(len(visited))


def recurse(node):
    global graph, weights
    score = 0
    for c in graph.edges[node]:
        score += graph.weights[(node,c)]*recurse(c)+graph.weights[(node,c)]
    return score

print(recurse('shiny gold bags'))
