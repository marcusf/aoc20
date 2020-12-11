import utils
from collections import defaultdict

input = utils.input_lines(generator=int, test=False)
jolts = sorted(input)
deltas = defaultdict(int)

deltas[jolts[0]] = 1
deltas[3] = 1

for (v1,v2) in utils.window(jolts):
    deltas[v2-v1]+=1

print(deltas[1]*deltas[3])

g = utils.Graph()

jolts = [0] + jolts + [jolts[-1]+3]

for i in range(len(jolts)):
    g.add_node(jolts[i])
    for v0 in jolts[i+1:]:
        if v0-jolts[i] <= 3:
            g.add_edge(jolts[i], v0, v0-jolts[i])


def node_cost(g, node, weights):
    if node in weights:
        return weights[node]

    if len(g.edges[node]) == 0:
        return 1
    else:
       s = sum([node_cost(g, v, weights) for v in g.edges[node]])
       weights[node] = s
       return s

print(node_cost(g,jolts[0], {}))
