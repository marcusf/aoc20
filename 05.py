from utils import input_lines, window
from re import sub

seats = [int(sub('[BR]','1', sub(r'[FL]','0',p)), 2) for p in input_lines()]
print(max(seats)) # A
print([lo+1 for lo, mid in window(sorted(seats)) if lo+1 != mid][0]) # B
