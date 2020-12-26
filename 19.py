import utils
import re

def parse(c): return c[1:-1] if c[0] == '"' else int(c)
def is_literal(c): return c == 'a' or  c == 'b'

input, data = utils.read_input_multi(delim_1='\n\n',delim_2='\n',test=False)
rules = {}
q = []

for row in input:
    k,v = row.split(': ')
    
    rules[k] = v
    if v == '"a"':
        rules[k] = 'a'
        q.append(k)
    elif v == '"b"':
        rules[k] = 'b'
        q.append(k)

#8: 42 | 42 8
#11: 42 31 | 42 11 31
# For part B, I eventually just gave up any clever attempt and regexped it. 
rules['8'] = '42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42'
rules['11'] = '42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31'

keys = list(rules.keys())
i = 0
while re.match('\d+',rules['0']):
    i+=1
    replace = q.pop(0)
    for rule in keys:
        exp = rules[rule]
        nexp = re.sub('(?:^|\s)'+replace+'(?:$|\s)',' (( '+rules[replace]+' )) ' if rules[replace] not in ['a','b'] else ' ' + rules[replace] + ' ', exp)
        nexp = re.sub('(?:^|\s)'+replace+'(?:$|\s)',' (( '+rules[replace]+' )) ' if rules[replace] not in ['a','b'] else ' ' + rules[replace] + ' ', nexp)
        if nexp != exp:
            rules[rule] = nexp
            q.append(rule)

print(rules['8'])
print(rules['11'])

rl = rules['0']
rl = re.sub(r'\d', '', rl)
rexp = '^' + rl.replace(' ','') + '$'
#print(rexp)

sum=0
for line in data:
    if re.match(rexp, line):
        sum+=1

print(sum)