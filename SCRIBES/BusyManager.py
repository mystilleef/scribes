class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("private-busy", self.__busy_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__busy = 0
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		return False

	def __set(self, busy):
		self.__busy = self.__busy + 1 if busy else self.__busy - 1
		if self.__busy < 0: self.__busy = 0
		busy = True if self.__busy else False
		self.__editor.emit("busy", busy)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, editor, busy):
		from gobject import idle_add
		idle_add(self.__set, busy)
		return False
