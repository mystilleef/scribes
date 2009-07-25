class Quiter(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("triggers-cleared", self.__cleared_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Quit flag must be True before system can quit.
		self.__quit = False
		# Cleared flag must be 2 before system can quit.
		self.__cleared = 0
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit_quit_signal(self):
		self.__cleared += 1
		if self.__quit is False: return False
		if self.__cleared != 2: return False
		self.__manager.emit("quit")
		self.__destroy()
		return False

	def __quit_cb(self, *args):
		self.__quit = True
		return False

	def __cleared_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__emit_quit_signal)
		return False
