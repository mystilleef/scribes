from string import punctuation, whitespace
DELIMETER = ("%s%s%s" % (punctuation, whitespace, "\x00")).replace("-", "").replace("_", "")

def is_delimeter(character): return character in DELIMETER

def is_not_delimeter(character): return not (character in DELIMETER)
