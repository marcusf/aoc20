from itertools import count

card_pk, door_pk, modulo = 8335663, 8614349, 20201227

card_ls = 0
for i in count():
    if card_pk == pow(7, i, modulo):
        card_ls = i
        break

print(pow(door_pk, card_ls, modulo))

