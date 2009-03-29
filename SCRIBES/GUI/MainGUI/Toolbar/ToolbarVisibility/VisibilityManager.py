class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("minimal-mode", self.__minimal_mode_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit(self, minimal_mode):
		emit = self.__manager.emit
		emit("hide") if minimal_mode else emit("show")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __minimal_mode_cb(self, manager, minimal_mode):
		from gobject import idle_add
		idle_add(self.__emit, minimal_mode)
		return False
