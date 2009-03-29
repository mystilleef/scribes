from gtk import MenuToolButton

class Button(MenuToolButton):

	def __init__(self, editor):
		editor.response()
		from gtk import STOCK_OPEN
		MenuToolButton.__init__(self, STOCK_OPEN)
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
		self.set_property("name", "OpenToolButton")
		self.set_property("sensitive", False)
		#self.set_tooltip(editor.tip, open_button_tip)
		from RecentMenu import RecentMenu
		self.set_menu(RecentMenu(self.__editor))
#		self.set_arrow_tooltip(editor.tip, recent_menu_tip, recent_menu_tip)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__editor.response()
		self.__editor.trigger("show_open_dialog")
		self.__editor.response()
		return False
