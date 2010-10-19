from gettext import gettext as _

class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def previous_paragraph(self):
		cursor_iterator = self.__editor.cursor
		current_line = cursor_iterator.get_line()
		try:
			if current_line == 0: raise RuntimeError
			line = self.__find_empty_line(cursor_iterator)
			if line is None: raise ValueError
			self.__jump_to_line(line)
			message = _("Moved to previous paragraph")
			self.__editor.update_message(message, "pass")
		except RuntimeError:
			message = _("No previous paragraph")
			self.__editor.update_message(message, "fail")
		except ValueError:
			self.__jump_to_line(0)
		return

	def next_paragraph(self):
		number_of_lines = self.__buffer.get_line_count()
		cursor_iterator = self.__editor.cursor
		current_line = cursor_iterator.get_line()
		try:
			if current_line == number_of_lines-1: raise RuntimeError
			line = self.__find_empty_line(cursor_iterator, False)
			if line is None: raise ValueError
			self.__jump_to_line(line)
			message = _("Moved to next paragraph")
			self.__editor.update_message(message, "pass")
		except RuntimeError:
			message = _("No next paragraph")
			self.__editor.update_message(message, "fail")
		except ValueError:
			self.__jump_to_line(number_of_lines-1)
		return

	def select_paragraph(self):
		try:
			begin, end = self.__get_paragraph_position()
			self.__buffer.select_range(begin, end)
			message = _("Selected paragraph")
			self.__editor.update_message(message, "pass")
		except RuntimeError:
			message = _("No paragraph found")
			self.__editor.update_message(message, "fail")
		return

	def reflow_paragraph(self):
		if self.__is_readonly(): return
		try:
			start, end = self.__get_paragraph_position()
		except RuntimeError:
			message = _("No paragraph found")
			self.__editor.update_message(message, "fail")
			return
		text = start.get_text(end)
		try:
			text = self.__reflow_text(text)
		except RuntimeError:
			message = _("No text found")
			self.__editor.update_message(message, "fail")
			return
		self.__buffer.begin_user_action()
		self.__buffer.delete(start, end)
		self.__buffer.insert_at_cursor(text)
		self.__buffer.end_user_action()
		message = _("Reflowed paragraph")
		self.__editor.update_message(message, "pass")
		return

	def destroy(self):
		del self
		self = None
		return


	def __get_paragraph_position(self):
		iterator = self.__get_current_line_iterator()
		if iterator.is_start() and iterator.is_end(): raise RuntimeError
		if self.__is_empty_line(iterator): raise RuntimeError
		first_paragraph_line = self.__find_empty_line(iterator)
		if first_paragraph_line is None:
			begin, end = self.__buffer.get_bounds()
		else:
			begin = self.__buffer.get_iter_at_line(first_paragraph_line)
			begin.forward_line()
		second_paragraph_line = self.__find_empty_line(iterator, False)
		if second_paragraph_line is None:
			start, end = self.__buffer.get_bounds()
		else:
			end = self.__buffer.get_iter_at_line(second_paragraph_line)
			end.backward_line()
			end.forward_to_line_end()
		return begin, end

	def __get_current_line_iterator(self):
		iterator = self.__editor.cursor
		if iterator.starts_line(): return iterator
		line = iterator.get_line()
		return self.__buffer.get_iter_at_line(line)

	def __find_empty_line(self, iterator, backwards=True):
		while True:
			if backwards:
				if not iterator.backward_line(): return None
			else:
				if not iterator.forward_line(): return None
			if self.__is_empty_line(iterator): return iterator.get_line()
		return None

	def __is_empty_line(self, iterator):
		if iterator.ends_line(): return True
		temporary_iterator = iterator.copy()
		temporary_iterator.forward_to_line_end()
		text = iterator.get_text(temporary_iterator)
		if not text: return True
		if text.isspace(): return True
		return False

	def __jump_to_line(self, line):
		iterator = self.__buffer.get_iter_at_line(line)
		self.__buffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		return

	def __reflow_text(self, text):
		if not text or text.isspace(): raise RuntimeError
		text_lines = text.split("\n")
		indentation = self.__get_indentation(text_lines[0])
		wrap_width = self.__calculate_wrap_width(indentation)
		reflowed_lines = []
		remainder = ""
		line = " ".join(text_lines)
		line = line.replace("\t", " ")
		line = line.strip()
		line = self.__respace_line(line)
		if len(line) > wrap_width:
			while True:
				new_line, remainder = self.__shorten_line(line, wrap_width)
				reflowed_lines.append(new_line)
				if len(remainder) < wrap_width: break
				line = remainder.strip()
		else:
			reflowed_lines.append(line)
		if remainder: reflowed_lines.append(remainder)
		indented_reflowed_lines = self.__indent_lines(reflowed_lines, indentation)
		return "\n".join(indented_reflowed_lines)

	def __shorten_line(self, line, wrap_width):
		from textwrap import wrap
		line = line.strip()
		new_lines = wrap(line, wrap_width, expand_tabs=False, replace_whitespace=False)
		new_line = new_lines[0]
		remainder = " ".join(new_lines[1:])
		return new_line.strip(), remainder.strip()

	def __indent_lines(self, reflowed_lines, indentation):
		if len(reflowed_lines) < 2: return reflowed_lines
		indent_line = lambda x: indentation + x.strip()
		indented_lines = map(indent_line, reflowed_lines)
		return indented_lines

	def __get_indentation(self, line):
		indentation_list = []
		for char in line:
			if not (char in [" ", "\t"]): break
			indentation_list.append(char)
		return "".join(indentation_list)

	def __respace_line(self, line):
		line = line.split(" ")
		while True:
			try:
				line.remove("")
			except ValueError:
				break
		return " ".join(line)

	def __calculate_wrap_width(self, indentation):
		width = self.__get_right_margin_width()
		if not indentation: return width
		tab_width = self.__get_tab_width()
		number_of_tab_chars = indentation.count("\t")
		number_of_space_chars = indentation.count(" ")
		width = width - (number_of_space_chars + (number_of_tab_chars * tab_width))
		return width

	def __get_tab_width(self):
		return self.__editor.textview.get_tab_width()

	def __is_readonly(self):
		if not (self.__editor.readonly): return False
		message = _("Editor is in readonly mode")
		self.__editor.update_message(message, "fail")
		return True

	def __get_right_margin_width(self):
		return self.__editor.textview.get_right_margin_position()

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.reflow_paragraph)
			bind(self.next_paragraph)
			bind(self.previous_paragraph)
			bind(self.select_paragraph)
			bind(self.__reflow_text)
			bind(self.__shorten_line)
			bind(self.__respace_line)
			bind(self.__indent_lines)
			bind(self.__calculate_wrap_width)
			bind(self.__get_paragraph_position)
			bind(self.__get_current_line_iterator)
			bind(self.__find_empty_line)
			bind(self.__is_empty_line)
			bind(self.__jump_to_line)
		except ImportError:
			pass
		return False
