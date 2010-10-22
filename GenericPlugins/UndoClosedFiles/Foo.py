from SCRIBES.SignalConnectionManager import SignalManager

class Foo(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __foo(self):
		message = "Witness the awesome power of Foo!"
		title = "Foo Power"
		# Update the message bar.
		self.__editor.update_message(message, "yes", 10)
		# Show a window containing Foo message.
		self.__editor.show_info(title, message, self.__editor.window)
		return False

	def __activate_cb(self, *args):
		self.__foo()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
