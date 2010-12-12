def get_iter(marks, textbuffer):
	_iter = textbuffer.get_iter_at_mark
	return _iter(marks[0]), _iter(marks[1])
