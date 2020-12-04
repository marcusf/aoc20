import utils
import re

# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)

def a(inp):
	required = set(['byr','iyr','eyr','hgt','hcl','ecl','pid']) # ,'cid'])
	inp = [s.replace('\n',' ').split(' ') for s in inp]

	valid = 0
	for row in inp:
		keys = set([k.split(':')[0] for k in row])
		if len(required - keys) == 0:
			valid += 1

	print(valid)

#byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.


def isint(i):
	try:
		int(i)
	except:
		return False
	return True

def is_invalid_int(key, low, up):
	if not isint(key):
		return True
	i = int(key)
	if i < low or i > up:
		return True
	return False

def is_invalid_hgt(key):
	number, unit = key[:-2], key[-2:] 
	if unit == 'cm':
		return is_invalid_int(number, 150, 193)
	elif unit == 'in':
		return is_invalid_int(number, 59, 76)
	else:
		return True

def is_invalid_hcl(key): return re.match(r'^#[0-9a-f]{6}$', key) == None

def is_invalid_ecl(key):
	ecls = set('amb blu brn gry grn hzl oth'.split(' '))
	return not key in ecls

def is_invalid_pid(key): return re.match(r'^[0-9]{9}$', key) == None

def b(inp):
	required = set(['byr','iyr','eyr','hgt','hcl','ecl','pid']) # ,'cid'])
	inp = [s.replace('\n',' ').split(' ') for s in inp]

	valid = 0
	for row in inp:
		kvs = dict([k.split(':') for k in row])
		invalid = False

		if len(required - kvs.keys()) == 0:
			invalid |= is_invalid_int(kvs['byr'], 1920, 2002)			
			invalid |= is_invalid_int(kvs['iyr'], 2010, 2020) 
			invalid |= is_invalid_int(kvs['eyr'], 2020, 2030)
			invalid |= is_invalid_hgt(kvs['hgt'])
			invalid |= is_invalid_hcl(kvs['hcl'])
			invalid |= is_invalid_ecl(kvs['ecl'])
			invalid |= is_invalid_pid(kvs['pid'])
			if not invalid:
				valid+=1

	print(valid)

inp = utils.read_input(delim='\n\n', generator=str, test=False)
a(inp)
b(inp)