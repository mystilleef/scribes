from SCRIBES.SignalConnectionManager import SignalManager

class Opener(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "open-files", self.__open_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __open_cb(self, manager, files):
		self.__editor.open_files(files)
		return False
