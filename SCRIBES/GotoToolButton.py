from gtk import ToolButton

class Button(ToolButton):

	def __init__(self, editor):
		ToolButton.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("clicked", self.__clicked_cb)
		editor.register_object(self)
		self.show()
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set_properties(self):
		from gtk import STOCK_JUMP_TO
		self.set_property("stock-id", STOCK_JUMP_TO)
		self.set_property("name", "GotoToolButton")
		self.set_property("sensitive", False)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		print "Not yet implemented"
		return False
