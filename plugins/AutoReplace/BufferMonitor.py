class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = editor.textbuffer.connect_after("insert-text", self.__insert_cb)
		self.__sigid3 = manager.connect("dictionary", self.__dictionary_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__list = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __get_word(self):
		if not (self.__editor.cursor.get_char() in (" ", "\t", "\n")): return None
		start = self.__editor.backward_to_line_begin()
		text = self.__editor.textbuffer.get_text(start, self.__editor.cursor)
		if not text: return None
		if text[-1] in (" ", "\t"): return None
		return text.split()[-1]

	def __check(self):
		try:
			found = lambda word: self.__manager.emit("match-found", word)
			nofound = lambda: self.__manager.emit("no-match-found")
			word = self.__get_word()
			if word is None: raise ValueError
			found(word) if word in self.__list else nofound()
		except ValueError:
			nofound()
		return False

	def __precompile_methods(self):
		methods = (self.__insert_cb, self.__check, self.__get_word)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __insert_cb(self, *args):
		self.__check()
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__list = dictionary.keys()
		return False
