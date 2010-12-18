from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "execute", self.__freeze_cb)
		self.connect(manager, "removed-placeholders", self.__thaw_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__frozen = False
		return

	def __freeze(self):
		if self.__frozen: return False
		self.__editor.freeze()
		self.__frozen = True
		return False

	def __thaw(self):
		if self.__frozen is False: return False
		self.__editor.thaw()
		self.__frozen = False
		return False

	def __freeze_cb(self, *args):
		self.__freeze()
		return False

	def __thaw_cb(self, *args):
		self.__thaw()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
