def unindent(sourceview):
	lines_unindented = []
	sourceview.set_property("editable", False)
	sourcebuffer = sourceview.get_property("buffer")
	cursor_iterator = sourcebuffer.get_iter_at_mark(sourcebuffer.get_insert())
	line_number = cursor_iterator.get_line()
	try:
		begin_selection, end_selection = sourcebuffer.get_selection_bounds()
		if begin_selection.get_line() == end_selection.get_line():
			sourcebuffer.begin_user_action()
			result = unindent_line(sourceview, begin_selection.get_line())
			sourcebuffer.end_user_action()
			if result:
				lines_unindented.append(line_number)
		else:
			use_response = False
			begining_line = begin_selection.get_line()
			end_line = end_selection.get_line()
			if end_line - begining_line > 1000:
				use_response = True
#				from SCRIBES.utils import response
			sourcebuffer.begin_user_action()
			for line in range(begining_line, end_line+1):
#				if use_response:
#					response()
				result = unindent_line(sourceview, line)
				if result:
					lines_unindented.append(line)
			sourcebuffer.end_user_action()
	except ValueError:
		sourcebuffer.begin_user_action()
		result = unindent_line(sourceview, line_number)
		sourcebuffer.end_user_action()
		if result:
			lines_unindented.append(line_number)
	sourceview.set_property("editable", True)
	return lines_unindented

def unindent_line(sourceview, line_number):
	sourcebuffer = sourceview.get_property("buffer")
	use_spaces = sourceview.get_property("insert-spaces-instead-of-tabs")
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
	if use_spaces:
		new_spaces = []
		if number_of_tabs:
			for space in range(tab_width * number_of_tabs):
				new_spaces.append(" ")
		if number_of_spaces:
			new_spaces += space_list
		total_number_of_spaces = len(new_spaces)
		if total_number_of_spaces % tab_width:
			for space in range(total_number_of_spaces % tab_width):
				new_spaces.remove(" ")
		else:
			for space in range(tab_width):
				new_spaces.remove(" ")
		string = "".join(new_spaces)
	else:
		if not number_of_spaces:
			tab_list.remove("\t")
		else:
			if number_of_spaces > tab_width:
				tabs = number_of_spaces / tab_width
				tab_list.append("\t" * tabs)
		string = "".join(tab_list)
	sourcebuffer.delete(begin_position, transition_position)
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	sourcebuffer.insert(begin_position, string)
	return True
