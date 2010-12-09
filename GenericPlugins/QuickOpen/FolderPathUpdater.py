from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "parent-path", self.__parent_cb)
		self.connect(manager, "show", self.__show_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "enumeration-error", self.__error_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__path = ""
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, parent=False):
		try:
			pwduri = self.__path if self.__path else self.__editor.pwd_uri
			from gio import File
			self.__path = File(pwduri).get_parent().get_uri() if parent else pwduri
			self.__manager.emit("current-path", self.__path)
		except AttributeError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __parent_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, True)
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False

	def __hide_cb(self, *args):
		self.__path = ""
		return False

	def __error_cb(self, *args):
		self.__path = ""
		from gobject import timeout_add
		timeout_add(1000, self.__update)
		return False
