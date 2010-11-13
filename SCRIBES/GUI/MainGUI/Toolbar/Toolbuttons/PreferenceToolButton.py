from gtk import MenuToolButton

class Button(MenuToolButton):

	def __init__(self, editor):
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

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.__editor.unregister_object(self)
		del self
		return

	def __set_properties(self):
		from ..Utils import never_focus
		never_focus(self)
		self.set_property("name", "PreferenceToolButton")
		self.set_property("sensitive", False)
		from gtk import Menu
		self.set_property("menu", Menu())
		from gettext import gettext as _
		from gtk import Tooltips
#		menu_tip = _("Advanced configuration editors")
#		self.set_arrow_tooltip(Tooltips(), menu_tip, menu_tip)
		self.set_tooltip_text(_("Show window to customize the editor (F12)"))
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__editor.trigger("show-preferences-window")
		return False
