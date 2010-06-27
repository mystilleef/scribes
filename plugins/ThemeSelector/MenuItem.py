from gettext import gettext as _

class MenuItem(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__menuitem.set_property("name", "Theme Selector MenuItem")
		self.__sigid1 = self.__menuitem.connect("activate", self.__activate_cb)
		editor.add_to_pref_menu(self.__menuitem)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import STOCK_SELECT_COLOR
		message = _("Theme Selector")
		self.__menuitem = editor.create_menuitem(message, STOCK_SELECT_COLOR)
		return

	def destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem)
		self.__editor.remove_from_pref_menu(self.__menuitem)
		self.__menuitem.destroy()
		del self
		self = None
		return

	def __activate_cb(self, menuitem):
		self.__editor.trigger("show-theme-selector")
		return False
