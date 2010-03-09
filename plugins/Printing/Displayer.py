from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(self.__manager, "destroy", self.__destroy_cb)
		self.connect(self.__manager, "show", self.__show_cb)
		self.connect(self.__manager, "print-dialog-is-visible", self.__visible_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__visible = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __show(self):
		if self.__visible: return False
		from PrintDialog import Dialog
		Dialog(self.__manager, self.__editor).show()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		return False
