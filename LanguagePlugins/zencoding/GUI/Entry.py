from SCRIBES.SignalConnectionManager import SignalManager

class Entry(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__quit_cb)
		self.connect(manager, "mapped", self.__show_cb)
		self.connect(self.__entry, "activate", self.__activate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_object("Entry")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __show(self):
		self.__editor.response()
		self.__entry.grab_focus()
		self.__editor.response()
		return False

	def __activate(self):
		abbreviation = self.__entry.get_text()
		self.__manager.emit("hide")
		self.__manager.emit("wrap-abbreviation", abbreviation)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False
