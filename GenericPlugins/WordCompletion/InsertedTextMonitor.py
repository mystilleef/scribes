from SCRIBES.SignalConnectionManager import SignalManager
from Utils import is_delimeter

WORDS_BEFORE_CURSOR = 2

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "match-found", self.__match_found_cb)
		self.connect(manager, "no-match-found", self.__no_match_found_cb)
		self.connect(manager, "inserting-text", self.__inserting_cb)
		self.connect(manager, "inserted-text", self.__inserted_cb)
		self.connect(self.__view, "backspace", self.__hide_cb)
		self.connect(self.__view, "cut-clipboard", self.__hide_cb)
		self.connect(self.__view, "paste-clipboard", self.__hide_cb)
		self.connect(self.__view, "delete-from-cursor", self.__hide_cb)
		self.connect(self.__view, "move-cursor", self.__hide_cb)
		self.connect(self.__view, "move-viewport", self.__hide_cb)
		self.connect(self.__view, "page-horizontally", self.__hide_cb)
		self.connect(self.__view, "populate-popup", self.__hide_cb)
		self.connect(self.__view, "move-focus", self.__hide_cb)
		self.connect(self.__view, "button-press-event", self.__hide_cb)
		self.connect(self.__view, "focus-out-event", self.__hide_cb)
		self.connect(self.__buffer, "insert-text", self.__insert_text_cb, True)
		self.connect(self.__buffer, "insert-text", self.__insert_cb)
		self.connect(self.__buffer, "delete-range", self.__hide_cb, True)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__valid = False
		self.__is_active = False
		self.__is_visible = False
		self.__inserting = False
		self.__smark, self.__emark = None, None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __send_valid_string_async(self):
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(350, self.__send_valid_string, priority=PRIORITY_LOW)
		return False

	def __send_valid_string(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__send, priority=PRIORITY_LOW)
		return False

	def __send(self):
		string = self.__get_word_before_cursor()
		self.__emit_valid(string) if string else self.__emit_invalid()
		return False

	def __get_word_before_cursor(self):
		self.__editor.refresh(False)
		iterator = self.__editor.cursor.copy()
		start = self.__backward_to_word_begin(iterator.copy())
		end = self.__forward_to_word_end(iterator.copy())
		word = self.__buffer.get_text(start, end).strip()
		if len(word) > WORDS_BEFORE_CURSOR: return word
		return None

	def __is_valid_character(self, character):
		self.__editor.refresh(False)
		from string import whitespace
		if character in whitespace: return False
		return character.isalpha() or character.isdigit() or (character in ("-", "_"))

	def __backward_to_word_begin(self, iterator):
		self.__editor.refresh(False)
		if iterator.starts_line(): return iterator
		iterator.backward_char()
		while self.__is_valid_character(iterator.get_char()):
			self.__editor.refresh(False)
			iterator.backward_char()
			if iterator.starts_line(): return iterator
		iterator.forward_char()
		return iterator

	def __forward_to_word_end(self, iterator):
		self.__editor.refresh(False)
		if iterator.ends_line(): return iterator
		if not self.__is_valid_character(iterator.get_char()): return iterator
		while self.__is_valid_character(iterator.get_char()):
			self.__editor.refresh(False)
			iterator.forward_char()
			if iterator.ends_line(): return iterator
		return iterator

	def __emit_valid(self, string):
		self.__valid = True
		self.__manager.emit("valid-string", string)
		return False

	def __emit_invalid(self):
		if self.__valid is False: return
		self.__manager.emit("invalid-string")
		self.__valid = False
		return False

	def __compile(self):
		methods = (
			self.__insert_cb, self.__insert_text_cb, self.__get_word_before_cursor,
			self.__backward_to_word_begin, self.__forward_to_word_end, self.__is_valid_character
		)
		self.__editor.optimize(methods)
		return False

	def __insert_cb(self, textbuffer, iterator, text, length):
		self.__remove_timer()
		if length > 1 or is_delimeter(text): self.__manager.emit("no-match-found")
		return False

	def __insert_text_cb(self, textbuffer, iterator, text, length):
		if self.__inserting: return False
		if length > 1: return False
		if is_delimeter(text) or not is_delimeter(iterator.get_char()): return False
		self.__send() if self.__is_visible else self.__send_valid_string_async()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __hide_cb(self, *args):
		self.__emit_invalid()
		return False

	def __no_match_found_cb(self, *args):
		self.__is_visible = False
		return False

	def __match_found_cb(self, *args):
		self.__is_visible = True
		return False

	def __inserting_cb(self, *args):
		self.__inserting = True
		self.__emit_invalid()
		return False

	def __inserted_cb(self, *args):
		self.__inserting = False
		self.__emit_invalid()
		return False
