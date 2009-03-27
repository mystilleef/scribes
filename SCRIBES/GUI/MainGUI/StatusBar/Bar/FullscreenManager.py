class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("fullscreen", self.__fullscreen_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit(self, fullscreen):
		emit = self.__manager.emit
		emit("hide") if fullscreen else emit("database-query")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fullscreen_cb(self, editor, fullscreen):
		from gobject import idle_add
		idle_add(self.__emit, fullscreen)
		return False
