from SCRIBES.SignalConnectionManager import SignalManager

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "syntax-error", self.__syntax_cb)
		self.connect(manager, "tree-error", self.__tree_cb)
		self.connect(manager, "no-error-message", self.__no_error_cb)
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

	def __syntax_cb(self, manager, data):
		message = "Error: %s on line %s" % (data[2], data[0])
		self.__editor.update_message(message, "error", 10)
		return False

	def __tree_cb(self, manager, data):
		message = "Error: %s on line %s" % (data.message % data.message_args, data.lineno)
		self.__editor.update_message(message, "error", 10)
		return False

	def __no_error_cb(self, *args):
		message = _("No errors found")
		self.__editor.update_message(message, "yes")
		return False
