class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__textview = editor.textview
		return

	def __is_empty_line(self, iterator):
		text = self.__editor.get_line_text(iterator).strip(" \t\n")
		if not text: return True
		return False

	def __is_comment_line(self, iterator):
		text = self.__editor.get_line_text(iterator).strip(" \t")
		if text.startswith("#"): return True
		return False

	def __is_possible_start_block(self, current_indentation, pivot_indentation):
		if current_indentation < pivot_indentation: return True
		return False

	def __is_block_begin(self, iterator):
		iterator = self.__move_to_indented_character(iterator)
		if self.__is_primary_block_line(iterator): return True
		return False

	def __is_block_start(self, iterator, indentation):
		if self.__is_block_begin(iterator) is False: return False
		possible_start_block = self.__is_possible_start_block(iterator.get_line_offset(), indentation)
		if possible_start_block is False: return False
		return True

	def __is_class_block_start(self, iterator, indentation):
		if self.__is_class_line(iterator.copy()) is False: return False
		possible_start_block = self.__is_possible_start_block(iterator.get_line_offset(), indentation)
		if possible_start_block is False: return False
		return True

	def __is_def_block_start(self, iterator, indentation):
		if self.__is_def_line(iterator.copy()) is False: return False
		possible_start_block = self.__is_possible_start_block(iterator.get_line_offset(), indentation)
		if possible_start_block is False: return False
		return True

	def __is_past_block_end(self, iterator, indentation):
		if self.__is_secondary_block_line(iterator.copy()): return False
		iterator = self.__move_to_indented_character(iterator)
		offset = iterator.get_line_offset()
		if offset <= indentation: return True
		return False

	def __get_start_block(self, iterator):
		indentation = iterator.get_line_offset()
		while True:
			try:
				if self.__editor.is_empty_line(iterator): raise ValueError
				if self.__is_comment_line(iterator): raise ValueError
				if self.__is_block_start(iterator.copy(), indentation): break
#				if self.__is_inside_block(iterator.copy()): break
			except ValueError:
				pass
			success = iterator.backward_line()
			if success is False: raise ValueError
		iterator = self.__move_to_indented_character(iterator)
#		while iterator.get_char() in (" ", "\t"): iterator.forward_char()
		return iterator

	def __find_start_def_block(self, iterator):
		if self.__is_def_line(iterator.copy()): return self.__move_to_indented_character(iterator.copy())
		indentation = iterator.get_line_offset()
		while True:
			try:
				if self.__editor.is_empty_line(iterator): raise ValueError
				if self.__is_comment_line(iterator): raise ValueError
				if self.__is_def_block_start(iterator.copy(), indentation): break
			except ValueError:
				pass
			success = iterator.backward_line()
			if success is False: raise ValueError
		iterator = self.__move_to_indented_character(iterator)
		return iterator

	def __find_start_class_block(self, iterator):
		if self.__is_class_line(iterator.copy()): return self.__move_to_indented_character(iterator.copy())
		indentation = iterator.get_line_offset()
		while True:
			try:
				if self.__editor.is_empty_line(iterator): raise ValueError
				if self.__is_comment_line(iterator): raise ValueError
				if self.__is_class_block_start(iterator.copy(), indentation): break
			except ValueError:
				pass
			success = iterator.backward_line()
			if success is False: raise ValueError
		iterator = self.__move_to_indented_character(iterator)
		return iterator

	def __move_to_previous_block(self, iterator):
		indentation = iterator.get_line_offset()
		while True:
			try:
				success = iterator.backward_line()
				if success is False: raise TypeError
				if self.__editor.is_empty_line(iterator): raise ValueError
				if self.__is_comment_line(iterator): raise ValueError
				if self.__is_primary_block_line(iterator.copy()): break
#				if self.__is_inside_block(iterator.copy()): break
			except ValueError:
				pass
		iterator = self.__move_to_indented_character(iterator)
#		while iterator.get_char() in (" ", "\t"): iterator.forward_char()
		return iterator

	def __move_to_next_block(self, iterator):
		indentation = iterator.get_line_offset()
		while True:
			try:
				success = iterator.forward_line()
				if success is False: raise TypeError
				if self.__editor.is_empty_line(iterator): raise ValueError
				if self.__is_comment_line(iterator): raise ValueError
				if self.__is_primary_block_line(iterator.copy()): break
#				if self.__is_inside_block(iterator.copy()): break
			except ValueError:
				pass
		iterator = self.__move_to_indented_character(iterator)
#		while iterator.get_char() in (" ", "\t"): iterator.forward_char()
		return iterator

	def __move_to_indented_character(self, iterator):
		iterator = self.__editor.backward_to_line_begin(iterator)
		while iterator.get_char() in (" ", "\t"): iterator.forward_char()
		return iterator

	def __move_backward_to_inner_indentation(self, iterator, indentation):
		if indentation < iterator.get_line_offset(): return iterator
		while True:
			success = iterator.backward_line()
			if success is False: raise ValueError
			if self.__editor.is_empty_line(iterator): continue
			iterator = self.__move_to_indented_character(iterator)
			if indentation < iterator.get_line_offset(): break
		return iterator

	def __move_to_end_of_line(self, iterator):
		iterator = self.__editor.forward_to_line_end(iterator)
		while iterator.get_char() in (" ", "\t", "\n"): iterator.backward_char()
		iterator.forward_char()
		return iterator

	def __find_end_block(self, iterator):
		indentation = iterator.get_line_offset()
		while True:
			success = iterator.forward_line()
			if success is False: break
			if self.__editor.is_empty_line(iterator.copy()): continue
			if self.__is_comment_line(iterator.copy()): continue
			if self.__is_past_block_end(iterator.copy(), indentation): break
		iterator =	self.__move_backward_to_inner_indentation(iterator, indentation)
		iterator = self.__move_to_end_of_line(iterator)
		return iterator

	def __find_start_block(self, iterator):
		if self.__is_block_begin(iterator.copy()):
			iterator = self.__move_to_indented_character(iterator.copy())
		else:
			iterator = self.__get_start_block(iterator.copy())
		return iterator

	def __get_pivot_iterator(self):
		iterator = self.__editor.cursor
		# Search for non-empty lines.
		empty_or_comment = lambda x: self.__editor.is_empty_line(x) or self.__is_comment_line(x) or self.__line_starts_with_secondary_block_keyword(x)
		while empty_or_comment(iterator):
			success = iterator.backward_line()
			if success is False: break
		if empty_or_comment(iterator): raise TypeError # FIXME Raise an exception here instead.
		# Move iterator to the first non-whitespace character on the
		# line.
		iterator = self.__move_to_indented_character(iterator.copy())
		return iterator

	def __is_block_line(self, iterator):
		if self.__line_starts_with_block_keyword(iterator.copy()): return True
		return False

	def __is_primary_block_line(self, iterator):
		primary_block = self.__line_starts_with_primary_block_keyword(iterator.copy())
		has_block_colon = self.__has_block_line_colon(iterator.copy())
		if primary_block and has_block_colon: return True
		return False

	def __is_secondary_block_line(self, iterator):
		if self.__line_starts_with_secondary_block_keyword(iterator.copy()): return True
		return False

	def __line_starts_with_keyword(self, iterator):
		# Possible Python keywords found at the beginning of a line.
		keywords = ("del", "from", "while", "elif", "with", "assert",
			"else", "if", "pass", "yield", "break", "except", "import",
			"print", "class", "raise", "continue", "finally", "return",
			"def", "for", "try")
		return self.__token_in_keywords(iterator, keywords)

	def __line_starts_with_block_keyword(self, iterator):
		keywords = ("while", "elif", "with", "else", "if", "except",
			"class", "finally", "def", "for", "try")
		return self.__token_in_keywords(iterator, keywords)

	def __line_starts_with_primary_block_keyword(self, iterator):
		keywords = ("while", "with", "if", "class", "def", "for", "try")
		return self.__token_in_keywords(iterator, keywords)

	def __is_def_line(self, iterator):
		if self.__line_starts_with_primary_block_keyword(iterator) is False: return False
		keywords = ("def",)
		return self.__token_in_keywords(iterator.copy(), keywords)

	def __is_class_line(self, iterator):
		if self.__line_starts_with_primary_block_keyword(iterator) is False: return False
		keywords = ("class",)
		return self.__token_in_keywords(iterator.copy(), keywords)

	def __line_starts_with_secondary_block_keyword(self, iterator):
		keywords = ("else", "elif", "except", "finally")
		return self.__token_in_keywords(iterator, keywords)

	def __token_in_keywords(self, iterator, keywords):
		token = self.__get_first_token_on_line(iterator.copy())
		if token in keywords: return True
		return False

	def __has_block_line_colon(self, iterator):
		if self.__ends_with_colon(iterator.copy()): return True
		while True:
			success = iterator.forward_line()
			if success is False: return False
			if self.__line_starts_with_keyword(iterator): return False
			if self.__ends_with_colon(iterator.copy()): return True
		return True

	def __get_first_token_on_line(self, iterator):
		text = self.__strip_line_text(iterator)
		token = text.split(" ")[0].split(":")[0]
		return token

	def __ends_with_colon(self, iterator):
		text = self.__strip_line_text(iterator.copy())
		if text.endswith(":"): return True
		return False

	def __strip_line_text(self, iterator):
		text = self.__editor.get_line_text(iterator).strip(" \t\n")
		return text

########################################################################
#
#						Public Methods
#
########################################################################

	def select_block(self):
		try:
			# Point to start searching from.
			iterator = self.__get_pivot_iterator()
			start_block_iterator = self.__find_start_block(iterator)
			end_block_iterator = self.__find_end_block(start_block_iterator.copy())
			self.__editor.textbuffer.select_range(start_block_iterator, end_block_iterator)
			message = "Selected block"
			self.__editor.update_message(message, "yes")
			self.__editor.move_view_to_cursor()
		except ValueError:
			message = "Block not found"
			self.__editor.update_message(message, "no")
		except TypeError:
			message = "Block not found"
			self.__editor.update_message(message, "no")
		return True

	def next_block(self):
		try:
			iterator = self.__get_pivot_iterator()
			iterator = self.__move_to_next_block(iterator.copy())
			self.__editor.textbuffer.place_cursor(iterator)
			self.__editor.move_view_to_cursor(True)
			message = "Moved cursor to next block"
			self.__editor.update_message(message, "yes")
		except ValueError:
			message = "Next block not found"
			self.__editor.update_message(message, "no")
		except TypeError:
			message = "Next block not found"
			self.__editor.update_message(message, "no")
		return

	def previous_block(self):
		try:
			iterator = self.__get_pivot_iterator()
			iterator = self.__move_to_previous_block(iterator.copy())
			self.__editor.textbuffer.place_cursor(iterator)
			self.__editor.move_view_to_cursor(True)
			message = "Move cursor to previous block"
			self.__editor.update_message(message, "yes")
		except ValueError:
			message = "Previous block not found"
			self.__editor.update_message(message, "no")
		except TypeError:
			message = "Previous block not found"
			self.__editor.update_message(message, "no")
		return

	def select_class(self):
		try:
			# Point to start searching from.
			iterator = self.__get_pivot_iterator()
			start = self.__find_start_class_block(iterator.copy())
			end = self.__find_end_block(start.copy())
			end_line = end.get_line()
			current_line = self.__editor.cursor.get_line()
			if end_line < current_line: raise TypeError
			self.__buffer.select_range(start, end)
			message = "Selected class block"
			self.__editor.update_message(message, "yes")
		except ValueError:
			message = "Out of class block range"
			self.__editor.update_message(message, "no")
		except TypeError:
			message = "Out of class block range"
			self.__editor.update_message(message, "no")
		return

	def select_function(self):
		try:
			# Point to start searching from.
			iterator = self.__get_pivot_iterator()
			start = self.__find_start_def_block(iterator.copy())
			end = self.__find_end_block(start.copy())
			end_line = end.get_line()
			current_line = self.__editor.cursor.get_line()
			if end_line < current_line: raise TypeError
			self.__buffer.select_range(start, end)
			message = "Selected function block"
			self.__editor.update_message(message, "yes")
		except ValueError:
			message = "Out of function range"
			self.__editor.update_message(message, "no")
		except TypeError:
			message = "Out of function range"
			self.__editor.update_message(message, "no")
		return

	def end_of_block(self):
		try:
			# Point to start searching from.
			iterator = self.__get_pivot_iterator()
			start_block_iterator = self.__find_start_block(iterator)
			end_block_iterator = self.__find_end_block(start_block_iterator.copy())
			self.__editor.textbuffer.place_cursor(end_block_iterator)
			self.__editor.move_view_to_cursor(True)
			message = "Move cursor to end of block"
			self.__editor.update_message(message, "yes")
		except ValueError:
			message = "End block not found"
			self.__editor.update_message(message, "no")
		except TypeError:
			message = "End block not found"
			self.__editor.update_message(message, "no")
		return

	def destroy(self):
		del self
		self = None
		return
