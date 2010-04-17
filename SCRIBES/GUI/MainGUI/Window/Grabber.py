from SCRIBES.SignalConnectionManager import SignalManager

class Grabber(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(self.__window, "focus-in-event", self.__in_cb, True)
		self.connect(self.__window, "focus-out-event", self.__out_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.window
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __in_cb(self, *args):
		self.__window.grab_add()
		return False

	def __out_cb(self, *args):
		self.__window.grab_remove()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
