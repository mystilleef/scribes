def starts_word(iterator, pattern):
	iterator = iterator.copy()
	character = iterator.get_char()
	if not pattern.match(character): return False
	if iterator.starts_line(): return True
	iterator.backward_char()
	character = iterator.get_char()
	if pattern.match(character): return False
	return True

def ends_word(iterator, pattern):
	iterator = iterator.copy()
	if iterator.starts_line(): return False
	character = iterator.get_char()
	if pattern.match(character): return False
	iterator.backward_char()
	character = iterator.get_char()
	if pattern.match(character): return True
	return False

def inside_word(iterator, pattern):
	iterator = iterator.copy()
	if starts_word(iterator, pattern) or ends_word(iterator, pattern): return True
	character = iterator.get_char()
	if pattern.match(character): return True
	return False

def get_word_boundary(iterator, pattern):
	start = iterator.copy()
	end = iterator.copy()
	while starts_word(start, pattern) is False: start.backward_char()
	while ends_word(end, pattern) is False: end.forward_char()
	return start, end
