from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor)
		editor.set_data("in_fullscreen_mode", False)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "toggle-fullscreen", self.__toggle_cb)
		self.connect(editor, "fullscreen", self.__fullscreen_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__enabled = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __toggle(self):
		enable = False if self.__enabled else True
		self.__editor.emit("fullscreen", enable)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __toggle_cb(self, *args):
		self.__toggle()
		return False

	def __fullscreen_cb(self, editor, enable):
		self.__editor.set_data("in_fullscreen_mode", enable)
		self.__enabled = enable
		return False
