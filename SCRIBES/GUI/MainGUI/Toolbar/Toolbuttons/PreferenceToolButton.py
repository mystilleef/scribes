from gtk import MenuToolButton

class Button(MenuToolButton):

	def __init__(self, editor):
		editor.response()
		from gtk import STOCK_PREFERENCES
		MenuToolButton.__init__(self, STOCK_PREFERENCES)
		self.__init_attributes(editor)
		self.__set_properties()
		from PreferenceMenuManager import Manager
		Manager(editor, self.get_menu())
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
		self.set_property("name", "PreferenceToolButton")
		self.set_property("sensitive", False)
		from gtk import Menu
		self.set_property("menu", Menu())
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__editor.response()
		self.__editor.trigger("show_preference_dialog")
		self.__editor.response()
		return False
