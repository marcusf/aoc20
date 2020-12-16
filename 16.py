import utils
import re

specs, your, other = utils.read_input(delim='\n\n', test=False)
specs = specs.split('\n')
specs = { a: [int(b) for b in bs] for a, *bs in [re.match(r'^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)', s).groups() for s in specs]}

intervals = sorted([a for b in [[[lo1,h1],[lo2,hi2]] for lo1, h1, lo2, hi2 in specs.values()] for a in b])

sm = 0
valid_rows = []

for row in other.split('\n')[1:]:
    ns = [int(i) for i in row.split(',')]
    row_invalid = False
    for n in ns:
        invalid = True
        for (a,b) in intervals:
            if a <= n and b >= n:
                invalid = False
                break
        if invalid:
            row_invalid = True
            sm += n
    if not row_invalid:
        valid_rows.append(ns)
            
print('Answer to A:', sm)
valid_columns = [set(specs.keys()) for v in valid_rows[0]]

for row in valid_rows:
    for i, column in enumerate(row):
        potentially_valid = valid_columns[i]

        for col_spec in set(potentially_valid):
            l1, h1, l2, h2 = specs[col_spec]
            if not ((l1 <= column and h1 >= column) or (l2 <= column and h2 >= column)):
                valid_columns[i] -= set([col_spec])

cands = [[n,v] for n,v in enumerate(valid_columns)]

done = {}

while cands:
    cands = sorted(cands, key=lambda v: len(v[1]))
    col, vals = cands.pop(0)
    if len(vals) == 1:
        for i in range(len(cands)):
           cands[i][1] -= vals
        done[col] = vals.pop()
    else:
        print('kuken!')

result = 1
your = [int(y) for y in your.split('\n')[1].split(',')]
for k,v in done.items():
    if v.find('departure') == 0:
        result *= your[k]

print(result)
