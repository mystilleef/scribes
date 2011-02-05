from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(self.__view, "move-cursor", self.__response_cb)
		self.connect(self.__view, "move-cursor", self.__response_cb, True)
		self.connect(self.__view, "scroll-event", self.__response_cb)
		self.connect(self.__view, "scroll-event", self.__response_cb, True)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __response_cb(self, *args):
		self.__editor.refresh(False)
#		print "Move or scroll event calling refresh"
		return False
