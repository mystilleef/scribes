from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "execute", self.__begin_cb)
		self.connect(manager, "removed-placeholders", self.__end_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __begin_cb(self, *args):
		self.__editor.textbuffer.begin_user_action()
		return False

	def __end_cb(self, *args):
		self.__editor.textbuffer.end_user_action()
		return False
