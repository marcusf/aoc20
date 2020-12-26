import utils
from collections import defaultdict

def reverse_map(dct):
    rev = defaultdict(set)
    for k,v in dct.items():
        for val in v:
            rev[val].add(k)
    return rev

def logically_consistent(ingredient, allergen, allergens, recipes):
    allergens = dict(allergens)
    for k in list(allergens.keys()):
        allergens[k] = allergens[k] - set([ingredient])
    allergens[allergen] = set([ingredient])
    rev = reverse_map(allergens)

    for i, (ingredients, in_allergens) in enumerate(recipes):
        booked = set()
        for ing in ingredients:
            booked |= rev[ing]
        for alg in in_allergens:
            if alg not in booked:
                return False
    return True


input = utils.input_lines(test=False)
input = [(a.split(' '), [bb.replace(')','') for bb in b.split(', ')]) for a,b in [i.split(' (contains ') for i in input]]

recipes, reverse = defaultdict(set),defaultdict(set)
ingreds, allergs = set(), set()

for ingredients, allergerns in input:
    for ingredient in ingredients:
        ingreds.add(ingredient)
        for allergen in allergerns:
            allergs.add(allergen)
            recipes[ingredient].add(allergen)
            reverse[allergen].add(ingredient)

cant_allergens = set()
candidates = defaultdict(set)

for ingred in ingreds:
    reasonable = False
    for allerg in recipes[ingred]:
        if logically_consistent(ingred, allerg, reverse, input):
            candidates[ingred].add(allerg)
            resonable = True

cant_allergens = ingreds - set(candidates.keys())

ctr = 0
for ingredients, _ in input:
    ctr += sum([1 for ing in ingredients if ing in cant_allergens])

print(ctr)
canonical = {}

while candidates:
    k, v = list(sorted(candidates.items(), key=lambda i: len(i[1])))[0]
    del candidates[k]
    ingred = v.pop()
    canonical[k] = ingred
    for kk in list(candidates.keys()):
        candidates[kk] -= set([ingred])

print(','.join([v[0] for v in list(sorted(canonical.items(), key=lambda k: k[1]))]))