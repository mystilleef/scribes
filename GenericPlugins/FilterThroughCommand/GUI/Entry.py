from SCRIBES.SignalConnectionManager import SignalManager

class Entry(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "mapped", self.__show_cb, True)
		self.connect(manager, "fail", self.__sensitive_cb)
		self.connect(manager, "restored-cursor-position", self.__sensitive_cb, True)
		self.connect(manager, "update-database", self.__insensitive_cb)
		self.connect(manager, "output-mode", self.__sensitive_cb)
		self.connect(self.__entry, "changed", self.__changed_cb)
		self.connect(self.__entry, "activate", self.__activate_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_object("Entry")
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __show_cb(self, *args):
		self.__entry.grab_focus()
		return False

	def __changed_cb(self, *args):
		command = self.__entry.get_text().strip()
		self.__manager.emit("command", command)
		return False

	def __activate_cb(self, *args):
		self.__manager.emit("execute")
		self.__entry.set_property("sensitive", False)
		return False

	def __sensitive_cb(self, *args):
		self.__entry.set_property("sensitive", True)
		self.__entry.grab_focus()
		return False

	def __insensitive_cb(self, *args):
		self.__entry.set_property("sensitive", False)
		return False

	def __hide_cb(self, *args):
		self.__entry.set_property("sensitive", True)
		return False
