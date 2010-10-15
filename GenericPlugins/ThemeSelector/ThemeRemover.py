from SCRIBES.SignalConnectionManager import SignalManager

class Remover(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "remove-scheme", self.__remove_cb)
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __remove(self, scheme):
		filename = scheme.get_filename()
		from os.path import exists
		if not exists(filename): return False
		from os import remove
		remove(filename)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __remove_cb(self, manager, scheme):
		from gobject import idle_add
		idle_add(self.__remove, scheme, priority=9999)
		return False
