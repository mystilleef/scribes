from gtk import ToolButton

class Button(ToolButton):

	def __init__(self, editor):
		editor.response()
		ToolButton.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("clicked", self.__clicked_cb)
		self.show()
		editor.register_object(self)
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
		from ..Utils import never_focus
		never_focus(self)
		from gtk import STOCK_FIND_AND_REPLACE
		self.set_property("stock-id", STOCK_FIND_AND_REPLACE)
		self.set_property("name", "ReplaceToolButton")
		self.set_property("sensitive", False)
		from gettext import gettext as _
		self.set_tooltip_text(_("Show bar to search for and replace text"))
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__editor.response()
		self.__editor.trigger("show_replacebar")
		self.__editor.response()
		return False
