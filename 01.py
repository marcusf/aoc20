import utils

inp = utils.read_input(delim='\n')

for i in range(len(inp)):
	for j in range(i,len(inp)):
		if inp[i]+inp[j] == 2020:
			print(inp[i]*inp[j])

for i in range(len(inp)):
	for j in range(i,len(inp)):
		for k in range(j,len(inp)):
			if inp[i]+inp[j]+inp[k] == 2020:
				print(inp[i]*inp[j]*inp[k])