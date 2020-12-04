import utils

inp = utils.read_input_multi(delim_2=' ',generator=str)

valid_1, valid_2 = 0, 0

for (interval, char, passw) in inp:
	char = char[0]
	mini, maxi = [int(i) for i in interval.split('-')]
	count = sum([1 for c in passw if c == char])
	if count >= mini and count <= maxi:
		valid_1 += 1
	if (passw[mini-1] == char and passw[maxi-1] != char) or (passw[maxi-1] == char and passw[mini-1] != char):
		valid_2 += 1

print(valid_1)
print(valid_2)
