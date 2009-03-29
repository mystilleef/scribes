from gtk import ToolButton

class Button(ToolButton):

	def __init__(self, editor):
		editor.response()
		ToolButton.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("clicked", self.__clicked_cb)
		self.__sigid3 = editor.connect("redo", self.__redo_cb)
		self.__sigid4 = editor.connect("undo", self.__redo_cb)
		self.__sigid5 = editor.connect("bar-is-active", self.__active_cb)
		self.show()
		editor.register_object(self)
		editor.response()

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
		from ..Utils import never_focus
		never_focus(self)
		from gtk import STOCK_REDO
		self.set_property("stock-id", STOCK_REDO)
		self.set_property("name", "RedoToolButton")
		self.set_property("sensitive", False)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __sensitive(self):
		self.__editor.response()
		sensitive = True if self.__editor.textbuffer.can_redo() else False
		self.set_property("sensitive", sensitive)
		self.__editor.response()
		return False

	def __clicked_cb(self, *args):
		self.__editor.response()
		self.__editor.redo()
		self.__sensitive()
		self.__editor.response()
		return False

	def __redo_cb(self, *args):
		self.__sensitive()
		return False

	def __active_cb(self, editor, active):
		self.set_property("sensitive", False) if active else self.__sensitive()
		return False
