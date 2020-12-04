import utils

inp = utils.read_input_multi(delim_2=None, generator=str, test=False)

def a(inp):
	x, y, l = 0, 0, len(inp[0])
	trees = 0
	for y in range(len(inp)):
		if inp[y][x % l] == '#':
			trees += 1
		x += 3

	print(trees)


def b(inp):
	strats = [[1,1],[1,3],[1,5],[1,7],[2,1]]
	ly, lx = len(inp), len(inp[0])

	total_trees = 1

	for dy, dx in strats:
		x, trees = 0, 0
		for y in range(0, ly, dy):
			if inp[y][x % lx] == '#':
				trees += 1
			x += dx
		total_trees *= trees

	print(total_trees)

a(inp)
b(inp)