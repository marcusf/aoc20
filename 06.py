print(*map(sum, zip(*[(len(set.union(*p)), len(set.intersection(*p))) 
    for p in [list(map(set, l.split())) 
        for l in open('06.input', 'r').read().split('\n\n')]])))
