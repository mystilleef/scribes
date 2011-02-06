from re import UNICODE, LOCALE, compile
word_pattern = compile(r"[^-\w]", UNICODE|LOCALE)

def merge(d1, d2, merge=lambda x,y:x+y):
	"""
	Merges two dictionaries, non-destructively, combining
	values on duplicate keys as defined by the optional merge
	function.  The default behavior replaces the values in d1
	with corresponding values in d2.  (There is no other generally
	applicable merge strategy, but often you'll have homogeneous
	types in your dicts, so specifying a merge technique can be
	valuable.)

	Examples:

	>>> d1
	{'a': 1, 'c': 3, 'b': 2}
	>>> merge(d1, d1)
	{'a': 1, 'c': 3, 'b': 2}
	>>> merge(d1, d1, lambda x,y: x+y)
	{'a': 2, 'c': 6, 'b': 4}

	"""
	result = dict(d1)
	for k,v in d2.iteritems():
		if k in result:
			result[k] = merge(result[k], v)
		else:
			result[k] = v
	return result

def no_zero_value_dictionary(dictionary):
	return dict([(k,v) for k,v in dictionary.items() if v != 0])

def index(string, negative=False):
	from re import split
	words = split(word_pattern, string)
	words = (word for word in words if __is_valid(word))
	from collections import defaultdict
	dictionary = defaultdict(int)
	for string in words:
		dictionary[string] = dictionary[string] -1 if negative else dictionary[string] + 1
	return dictionary

def __is_valid(word):
	if len(word) < 4: return False
	if word.startswith("---"): return False
	if word.startswith("___"): return False
	return True
