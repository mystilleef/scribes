from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "result", self.__result_cb)
		self.connect(manager, "output-mode", self.__output_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__output_mode = "replace"
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __result_cb(self, manager, result):
		if self.__output_mode == "replace": return False
		self.__manager.emit("win")
		self.__manager.emit("hide")
		self.__editor.new(text=result)
		return False

	def __output_cb(self, manager, output):
		self.__output_mode = output
		return False
