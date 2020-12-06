from utils import read_input_multi
from operator import and_, or_
from functools import reduce

print([sum(l) for l in zip(*[(len(reduce(or_, c)), len(reduce(and_, c))) for c in [[set([c for c in p]) for p in g] for g in read_input_multi('\n\n','\n')]])])
