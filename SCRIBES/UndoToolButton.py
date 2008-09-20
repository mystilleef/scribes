from gtk import ToolButton

class Button(ToolButton):

	def __init__(self, editor):
		ToolButton.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("clicked", self.__clicked_cb)
		self.__sigid3 = self.__editor.connect("undo", self.__undo_cb)
		self.__sigid4 = self.__editor.connect("redo", self.__undo_cb)
		self.__sigid5 = self.__editor.connect("modified-file", self.__undo_cb)
		editor.register_object(self)
		self.show()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set_properties(self):
		from gtk import STOCK_UNDO
		self.set_property("stock-id", STOCK_UNDO)
		self.set_property("name", "UndoToolButton")
		self.set_property("sensitive", False)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __sensitive(self):
		sensitive = True if self.__editor.textbuffer.can_undo() else False
		self.set_property("sensitive", sensitive)
		return False

	def __clicked_cb(self, *args):
		self.__editor.undo()
		self.__sensitive()
		return False

	def __undo_cb(self, *args):
		self.__sensitive()
		return False
