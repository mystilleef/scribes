class Manager(object):
	"""
	This class (un)comments lines in several source code.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__has_selection = False
		self.__commented = False
		self.__readonly = False
		iterator = editor.cursor
		self.__selection_begin_index = None
		self.__selection_begin_line = None
		self.__selection_end_index = None
		self.__selection_end_line = None
		return

	def __backward_to_line_begin(self, iterator):
		if iterator.starts_line(): return iterator
		while True:
			iterator.backward_char()
			if iterator.starts_line(): break
		return iterator

	def __forward_to_line_end(self, iterator):
		if iterator.ends_line(): return iterator
		iterator.forward_to_line_end()
		return iterator

	def __get_selection_range(self):
		self.__has_selection = True
		begin, end = self.__buffer.get_selection_bounds()
		self.__selection_begin_index = begin.get_line_index()
		self.__selection_begin_line = begin.get_line()
		self.__selection_end_index = end.get_line_index()
		self.__selection_end_line = end.get_line()
		end_position = self.__forward_to_line_end(end)
		begin_position = self.__backward_to_line_begin(begin)
		return begin_position, end_position

	def __get_range(self):
		if self.__buffer.get_property("has-selection"): return self.__get_selection_range()
		iterator = self.__editor.cursor
		if iterator.starts_line() and iterator.ends_line(): return None
		end_position = self.__forward_to_line_end(iterator.copy())
		begin_position = self.__backward_to_line_begin(iterator)
		return begin_position, end_position

	def __get_first_nonwhitespace(self, string):
		if not string: return None
		string = string.strip(" \t")
		if not string: return None
		return string[0]

	def __line_is_comment(self, line):
		is_comment = True if self.__get_first_nonwhitespace(line) == "#" else False
		return is_comment

	def __should_comment(self, lines):
		should_comment = True
		for line in lines:
			if self.__line_is_comment(line) is False: continue
			should_comment = False
			break
		return should_comment

	def __comment_line(self, line):
		if self.__line_is_comment(line): return line
		line = "#" + line
		return line

	def __uncomment_line(self, line):
		while self.__line_is_comment(line):
			line = line.replace("#", "", 1)
		return line

	def __comment_lines(self, lines):
		return [self.__comment_line(line) for line in lines]

	def __uncomment_lines(self, lines):
		return [self.__uncomment_line(line) for line in lines]

	def __update_feedback_message(self):
		if self.__readonly:
			from i18n import msg5
			message = msg5
			self.__editor.update_message(message, "fail")
		else:
			if self.__commented:
				if self.__has_selection:
					from i18n import msg1
					message = msg1
				else:
					line = self.__editor.cursor.get_line() + 1
					from i18n import msg2
					message = msg2 % line
			else:
				if self.__has_selection:
					from i18n import msg3
					message = msg3
				else:
					line = self.__editor.cursor.get_line() + 1
					from i18n import msg4
					message = msg4 % line
			self.__editor.update_message(message, "pass")
		return

	def __reset_flags(self):
		self.__has_selection = False
		self.__commented = False
		self.__readonly = False
		return

	def toggle_comment(self):
		try:
			from Exceptions import ReadOnlyError
			if self.__editor.readonly: raise ReadOnlyError
			offset = self.__editor.cursor.get_offset()
			begin, end = self.__get_range()
			text = self.__buffer.get_text(begin, end)
			lines = text.split("\n")
			if self.__should_comment(lines):
				self.__commented = True
				lines = self.__comment_lines(lines)
				offset += 1
			else:
				self.__commented = False
				lines = self.__uncomment_lines(lines)
				# If line is not empty (offset - 1)
				if not (len(lines) == 1 and not lines[0]): offset -= 1
			text = "\n".join(lines)
			self.__buffer.place_cursor(begin)
			self.__buffer.delete(begin, end)
			self.__buffer.insert_at_cursor(text)
			if self.__has_selection:
				begin = self.__get_begin_selection()
				end = self.__get_end_selection()
				self.__buffer.select_range(begin, end)
			else:
				iterator = self.__buffer.get_iter_at_offset(offset)
				self.__buffer.place_cursor(iterator)
		except TypeError:
			self.__buffer.insert_at_cursor("#")
			self.__commented = True
			iterator = self.__buffer.get_iter_at_offset(offset)
			self.__buffer.place_cursor(iterator)
		except ReadOnlyError:
			self.__readonly = True
		finally:
			self.__update_feedback_message()
			self.__reset_flags()
		return

	def __get_begin_selection(self):
		iterator = self.__buffer.get_iter_at_line(self.__selection_begin_line)
		line_size = iterator.get_bytes_in_line()
		if self.__selection_begin_index >= line_size:
			begin = self.__forward_to_line_end(iterator)
			begin.forward_char()
		else:
			begin = self.__buffer.get_iter_at_line_index(self.__selection_begin_line, self.__selection_begin_index)
		if self.__commented:
			begin.forward_char()
		else:
			begin.backward_char()
		return begin

	def __get_end_selection(self):
		iterator = self.__buffer.get_iter_at_line(self.__selection_end_line)
		line_size = iterator.get_bytes_in_line()
		if self.__selection_end_index >= line_size:
			end = self.__forward_to_line_end(iterator)
			end.forward_char()
		else:
			end = self.__buffer.get_iter_at_line_index(self.__selection_end_line, self.__selection_end_index)
		if self.__commented:
			end.forward_char()
		else:
			end.backward_char()
		return end

	def destroy(self):
		del self
		self = None
		return
