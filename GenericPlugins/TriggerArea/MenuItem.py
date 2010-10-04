from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

class MenuItem(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.__menuitem.set_property("name", "Trigger Area MenuItem")
		self.connect(self.__menuitem, "activate", self.__activate_cb)
		editor.add_to_pref_menu(self.__menuitem)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import STOCK_SELECT_COLOR
		message = _("Trigger Area")
		self.__menuitem = editor.create_menuitem(message, STOCK_SELECT_COLOR)
		return

	def destroy(self):
		self.disconnect()
		self.__editor.remove_from_pref_menu(self.__menuitem)
		self.__menuitem.destroy()
		del self
		return

	def __activate_cb(self, menuitem):
		self.__editor.trigger("show-trigger-area-window")
		return False
