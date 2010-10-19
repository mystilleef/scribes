class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("readonly", self.__readonly_cb)
		editor.register_object(self)

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

	def __set(self):
		#FIXME: change image id.
		self.__manager.emit("set", "scribes")
		return False

	def __unset(self):
		#FIXME: change image id
		self.__manager.emit("unset", "scribes")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __readonly_cb(self, editor, readonly):
		from gobject import idle_add
		idle_add(self.__set if readonly else self.__unset, priority=9999)
		return False
