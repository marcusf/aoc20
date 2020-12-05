import utils
import re

def get_seat(code): return int(re.sub('[BR]','1', re.sub(r'[FL]','0',code)), 2)
seats = [get_seat(p) for p in utils.read_input(generator=str, delim='\n')]
print(max(seats)) # A
print([lo+1 for lo, mid in utils.window(sorted(seats)) if lo+1 != mid][0]) # B
