from SCRIBES.SignalConnectionManager import SignalManager

class Opener(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "selected-paths", self.__uris_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __uris_cb(self, manager, uris):
		self.__editor.open_files(uris)
		return False
