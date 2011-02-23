from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "visible", self.__visible_cb, True)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self, visible):
		self.__editor.emit("toolbar-is-visible", visible)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __visible_cb(self, manager, visible):
		from gobject import idle_add
		idle_add(self.__update, visible)
		return False
