def valid_selection(start, end):
	from string import punctuation, whitespace
	punctuation = punctuation.replace("_", "")
	valid_characters = punctuation + whitespace
	if not (end.get_char() in valid_characters): return False
	if start.starts_line(): return True
	start.backward_char()
	if not (start.get_char() in valid_characters): return False
	return True