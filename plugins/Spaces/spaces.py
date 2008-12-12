def convert_spaces_to_tabs(sourceview):
	converted_lines = []
	sourcebuffer = sourceview.get_property("buffer")
	begin, end = sourcebuffer.get_bounds()
	first_line = begin.get_line()
	last_line = end.get_line()
	sourcebuffer.begin_user_action()
	for line in xrange(first_line, last_line+1):
		result = convert_spaces_to_tabs_on_line(sourceview, line)
		if result:
			converted_lines.append(line)
	sourcebuffer.end_user_action()
	return converted_lines

def convert_spaces_to_tabs_on_line(sourceview, line_number):
	sourcebuffer = sourceview.get_property("buffer")
	tab_width = sourceview.get_property("tab-width")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	space_list = []
	tab_list = []
	while True:
		if transition_position.get_char() in (" "):
			space_list.append(" ")
		elif transition_position.get_char() in ("\t"):
			tab_list.append("\t")
		else:
			break
		transition_position.forward_char()
	if transition_position.equal(begin_position):
		return False
	number_of_spaces = len(space_list)
	number_of_tabs = len(tab_list)
	if not number_of_spaces:
		return False
	if number_of_spaces < tab_width:
		string = "".join(tab_list)
	else:
		tabs = number_of_spaces / tab_width
		tab_list.append("\t" * tabs)
		string = "".join(tab_list)
	sourcebuffer.delete(begin_position, transition_position)
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	sourcebuffer.insert(begin_position, string)
	return True

def convert_tabs_to_spaces(sourceview):
	converted_lines = []
	sourcebuffer = sourceview.get_property("buffer")
	begin, end = sourcebuffer.get_bounds()
	first_line = begin.get_line()
	last_line = end.get_line()
	sourcebuffer.begin_user_action()
	for line in xrange(first_line, last_line+1):
		result = convert_tabs_to_spaces_on_line(sourceview, line)
		if result: converted_lines.append(line)
	sourcebuffer.end_user_action()
	return converted_lines

def convert_tabs_to_spaces_on_line(sourceview, line_number):
	sourcebuffer = sourceview.get_property("buffer")
	tab_width = sourceview.get_property("tab-width")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	space_list = []
	tab_list = []
	while True:
		if transition_position.get_char() in (" "):
			space_list.append(" ")
		elif transition_position.get_char() in ("\t"):
			tab_list.append("\t")
		else:
			break
		transition_position.forward_char()
	if transition_position.equal(begin_position):
		return False
	number_of_spaces = len(space_list)
	number_of_tabs = len(tab_list)
	if number_of_tabs:
		for tab in tab_list:
			space_list.append(" " * tab_width)
	if not len(space_list):
		return False
	if number_of_spaces % tab_width:
		for space in xrange(number_of_spaces % tab_width):
			space_list.remove(" ")
	string = "".join(space_list)
	sourcebuffer.delete(begin_position, transition_position)
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	sourcebuffer.insert(begin_position, string)
	return True

def remove_trailing_spaces(sourceview):
	affected_lines = []
	sourcebuffer = sourceview.get_property("buffer")
	begin, end = sourcebuffer.get_bounds()
	first_line = begin.get_line()
	last_line = end.get_line()
	sourcebuffer.begin_user_action()
	for line in xrange(first_line, last_line+1):
		result = remove_trailing_spaces_on_line(sourceview, line)
		if result:
			affected_lines.append(line)
	sourcebuffer.end_user_action()
	return affected_lines

def remove_trailing_spaces_on_line(sourceview, line_number):
	sourcebuffer = sourceview.get_property("buffer")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	transition_position.forward_to_line_end()
	if transition_position.equal(begin_position): return False
	while True:
		transition_position.backward_char()
		if not transition_position.get_char() in (" ", "\t"):
			transition_position.forward_char()
			break
	if transition_position.equal(end_position): return False
	sourcebuffer.delete(transition_position, end_position)
	return True
