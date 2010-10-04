from re import U, M, L, escape, compile as compile_
DOUBLE_QOUTE_PATTERN = '".*?"'
SINGLE_QUOTE_PATTERN = "'.*?'"
flags = U|L
DOUBLE_QOUTE_RE = compile_(DOUBLE_QOUTE_PATTERN, flags)
SINGLE_QUOTE_RE = compile_(SINGLE_QUOTE_PATTERN, flags)

PAIR_CHARACTERS = ("(", "{", "[", "<", ")", "}", "]", ">", "\"", "'")
OPEN_PAIR_CHARACTERS = ("(", "{", "[", "<", "\"", "'")
CLOSE_PAIR_CHARACTERS = (")", "}", "]", ">", "\"", "'")
QUOTE_CHARACTERS = ("\"", "'")

def get_pair_for(character):
	if __is_pair(character) is False: return ""
	if character in OPEN_PAIR_CHARACTERS: return __get_close_pair_for(character)
	return __get_open_pair_for(character)

def is_open_pair(character):
	if __is_pair(character) is False: return False
	return character in OPEN_PAIR_CHARACTERS

def __is_pair(character):
	return character in PAIR_CHARACTERS

def __get_close_pair_for(open_character):
	close_pair_for = {"(": ")", "{": "}", "[": "]", "<": ">", "\"": "\"", "'": "'"}
	return close_pair_for[open_character]

def __get_open_pair_for(close_character):
	open_pair_for = {")": "(", "}": "{", "]": "[", ">": "<", "\"": "\"", "'": "'"}
	return open_pair_for[close_character]

