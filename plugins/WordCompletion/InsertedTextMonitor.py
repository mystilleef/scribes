WORDS_BEFORE_CURSOR = 2

class Monitor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__buffer.connect_after("insert-text", self.__insert_text_cb)
		self.__sigid3 = self.__buffer.connect("delete-range", self.__generic_hide_cb)
		self.__sigid4 = self.__view.connect("backspace", self.__generic_hide_cb)
		self.__sigid5 = self.__view.connect("cut-clipboard", self.__generic_hide_cb)
		self.__sigid6 = self.__view.connect("paste-clipboard", self.__generic_hide_cb)
		self.__sigid7 = self.__view.connect("delete-from-cursor", self.__generic_hide_cb)
		self.__sigid8 = self.__view.connect("move-cursor", self.__generic_hide_cb)
		self.__sigid9 = self.__view.connect("move-viewport", self.__generic_hide_cb)
		self.__sigid10 = self.__view.connect("page-horizontally", self.__generic_hide_cb)
		self.__sigid11 = self.__view.connect("populate-popup", self.__generic_hide_cb)
		self.__sigid12 = self.__view.connect("move-focus", self.__generic_hide_cb)
		self.__sigid13 = manager.connect("match-found", self.__match_found_cb)
		self.__sigid14 = manager.connect("no-match-found", self.__no_match_found_cb)
		self.__sigid15 = manager.connect("inserting-text", self.__inserting_cb)
		self.__sigid16 = manager.connect("inserted-text", self.__inserted_cb)
		self.__sigid17 = self.__view.connect("button-press-event", self.__generic_hide_cb)
		self.__sigid18 = self.__view.connect("focus-out-event", self.__generic_hide_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=555)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__valid = False
		self.__is_active = False
		self.__is_visible = False
		self.__inserting = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid4, self.__view)
		self.__editor.disconnect_signal(self.__sigid5, self.__view)
		self.__editor.disconnect_signal(self.__sigid6, self.__view)
		self.__editor.disconnect_signal(self.__sigid7, self.__view)
		self.__editor.disconnect_signal(self.__sigid8, self.__view)
		self.__editor.disconnect_signal(self.__sigid9, self.__view)
		self.__editor.disconnect_signal(self.__sigid10, self.__view)
		self.__editor.disconnect_signal(self.__sigid11, self.__view)
		self.__editor.disconnect_signal(self.__sigid12, self.__view)
		self.__editor.disconnect_signal(self.__sigid13, self.__manager)
		self.__editor.disconnect_signal(self.__sigid14, self.__manager)
		self.__editor.disconnect_signal(self.__sigid15, self.__manager)
		self.__editor.disconnect_signal(self.__sigid16, self.__manager)
		self.__editor.disconnect_signal(self.__sigid17, self.__view)
		self.__editor.disconnect_signal(self.__sigid18, self.__view)
		del self
		self = None
		return False

	def __send_valid_string_async(self):
		try:
			from gobject import idle_add, source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(375, self.__send_valid_string, priority=999999)
		return False

	def __send_valid_string(self):
		try:
			from gobject import timeout_add, source_remove, idle_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__send, priority=999999)
		return False

	def __is_valid_character(self, character):
		from string import whitespace
		if character in whitespace: return False
		return character.isalpha() or character.isdigit() or (character in ("-", "_"))

	def __backward_to_word_begin(self, iterator):
		if iterator.starts_line(): return iterator
		iterator.backward_char()
		while self.__is_valid_character(iterator.get_char()):
			iterator.backward_char()
			if iterator.starts_line(): return iterator
		iterator.forward_char()
		return iterator

	def __forward_to_word_end(self, iterator):
		if iterator.ends_line(): return iterator
		if not self.__is_valid_character(iterator.get_char()): return iterator
		while self.__is_valid_character(iterator.get_char()):
			iterator.forward_char()
			if iterator.ends_line(): return iterator
		return iterator

	def __get_word_before_cursor(self):
		iterator = self.__editor.cursor.copy()
		# If the cursor is in front of a valid character we ignore
		# word completion.
		if self.__is_valid_character(iterator.get_char()): return None
		if iterator.starts_line(): return None
		iterator.backward_char()
		if not self.__is_valid_character(iterator.get_char()): return None
		start = self.__backward_to_word_begin(iterator.copy())
		end = self.__forward_to_word_end(iterator.copy())
		word = self.__buffer.get_text(start, end).strip()
		if len(word) > WORDS_BEFORE_CURSOR: return word
		return None

	def __send(self):
		string = self.__get_word_before_cursor()
		self.__emit_valid(string) if string else self.__emit_invalid()
		return False

	def __emit_valid(self, string):
		self.__valid = True
		self.__manager.emit("valid-string", string)
		return False

	def __emit_invalid(self):
		if self.__valid is False: return
		self.__manager.emit("invalid-string")
		self.__valid = False
		return False

	def __insert_text_cb(self, textbuffer, iterator, text, length):
		try:
			if self.__inserting: return False
			if (length > 1): raise ValueError
			from string import whitespace
			if text in whitespace: raise ValueError
			self.__send() if self.__is_visible else self.__send_valid_string_async()
		except ValueError:
			self.__emit_invalid()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __generic_hide_cb(self, *args):
		self.__emit_invalid()
		return False

	def __no_match_found_cb(self, *args):
		self.__is_visible = False
		return False

	def __match_found_cb(self, *args):
		self.__is_visible = True
		return False #

	def __inserting_cb(self, *args):
		self.__inserting = True
		self.__emit_invalid()
		return False

	def __inserted_cb(self, *args):
		self.__inserting = False
		self.__emit_invalid()
		return False

	def __precompile_methods(self):
		methods = (self.__insert_text_cb, self.__get_word_before_cursor,
			self.__send, self.__send_valid_string,
			self.__send_valid_string_async, self.__is_valid_character,
			self.__forward_to_word_end, self.__backward_to_word_begin)
		self.__editor.optimize(methods)
		return False
