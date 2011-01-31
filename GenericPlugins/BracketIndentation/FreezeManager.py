from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "empty-brackets", self.__freeze_cb)
		self.connect(manager, "done", self.__thaw_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __freeze_cb(self, *args):
		self.__editor.freeze()
		return False

	def __thaw_cb(self, *args):
		self.__editor.thaw()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
