from gtk import MenuItem
from gettext import gettext as _

class PopupMenuItem(MenuItem):

	def __init__(self, editor):
		editor.response()
		MenuItem.__init__(self, _("Line En_dings"))
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = editor.textview.connect("focus-in-event", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import Menu
		self.__menu = Menu()
		self.__menuitem1 = self.__editor.create_menuitem(_("Convert to _Unix (alt + 1)"))
		self.__menuitem2 = self.__editor.create_menuitem(_("Convert to _Mac (alt + 2)"))
		self.__menuitem3 = self.__editor.create_menuitem(_("Convert to _Windows (alt + 3)"))
		return

	def __set_properties(self):
		self.set_property("name", "Line Endings Popup MenuItem")
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("line-endings-to-unix")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("line-endings-to-mac")
		else:
			self.__editor.trigger("line-endings-to-windows")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor.textview)
		self.__menu.destroy()
		self.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
