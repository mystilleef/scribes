from gettext import gettext as _
message = _("Autoreplace Editor")

class MenuItem(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__menuitem.props.name = "Autoreplace Editor MenuItem"
		self.__sigid1 = self.__menuitem.connect("activate", self.__activate_cb, editor)
		editor.add_to_pref_menu(self.__menuitem)

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import STOCK_PROPERTIES
		self.__menuitem = editor.create_menuitem(message, STOCK_PROPERTIES)
		return

	def destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem)
		self.__editor.remove_from_pref_menu(self.__menuitem)
		self.__menuitem.destroy()
		del self
		self = None
		return

	def __activate_cb(self, menuitem, editor):
		editor.trigger("show-autoreplace-dialog")
		return False
