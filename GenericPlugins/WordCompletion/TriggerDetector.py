from SCRIBES.SignalConnectionManager import SignalManager
from Utils import is_delimeter, is_not_delimeter

WORDS_BEFORE_CURSOR = 2

class Detector(SignalManager):

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
		self.__sigid1 = self.connect(self.__buffer, "insert-text", self.__insert_text_cb, True)
		self.__sigid2 = self.connect(self.__buffer, "insert-text", self.__insert_cb)
		self.connect(self.__buffer, "delete-range", self.__hide_cb, True)
		self.connect(manager, "enable-word-completion", self.__completion_cb)
		self.__block()
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__is_active = False
		self.__is_visible = False
		self.__inserting = False
		self.__blocked = False
		self.__lmark, self.__rmark = manager.get_data("InsertionMarks")
		return

	def __send(self):
		string = self.__get_word_before_cursor()
		self.__manager.emit("generate", string) if string else self.__emit_invalid()
		return False

	def __send_idle(self):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__send, priority=PRIORITY_LOW)
		return False

	def __send_timeout(self):
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(500, self.__send_idle, priority=PRIORITY_LOW)
		return False

	def __get_word_before_cursor(self):
		start = self.__buffer.get_iter_at_mark(self.__lmark)
		end = self.__buffer.get_iter_at_mark(self.__rmark)
		word = self.__buffer.get_text(start, end).strip()
		if len(word) > WORDS_BEFORE_CURSOR: return word
		return None

	def __emit_invalid(self):
		self.__manager.emit("no-match-found")
		return False

	def __block(self):
		if self.__blocked: return False
		self.__buffer.handler_block(self.__sigid1)
		self.__buffer.handler_block(self.__sigid2)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__buffer.handler_unblock(self.__sigid1)
		self.__buffer.handler_unblock(self.__sigid2)
		self.__blocked = False
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __compile(self):
		methods = ( self.__insert_cb, self.__insert_text_cb, self.__get_word_before_cursor, )
		self.__editor.optimize(methods)
		return False

	def __completion_cb(self, manager, enable_word_completion):
		self.__unblock() if enable_word_completion else self.__block()
		return False

	def __insert_cb(self, textbuffer, iterator, text, length):
		
		self.__remove_timer()
		if length > 1 or is_delimeter(text): self.__manager.emit("no-match-found")
		return False

	def __insert_text_cb(self, textbuffer, iterator, text, length):
		if self.__inserting or self.__lmark is None or length > 1: return False
		if is_delimeter(text) or is_not_delimeter(iterator.get_char()): return False
		self.__remove_timer()
		self.__send() if self.__is_visible else self.__send_timeout()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
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
