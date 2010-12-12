from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "result", self.__result_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __result_cb(self, manager, result):
		self.__manager.emit("win")
		self.__manager.emit("hide")
		self.__editor.new(text=result)
		return False
