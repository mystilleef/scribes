from gettext import gettext as _
from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		editor.response()
		ImageMenuItem.__init__(self, _("S_paces"))
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__view.connect("focus-in-event", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__view = editor.textview
		self.__editor = editor
		from gtk import Menu, Image
		self.__menu = Menu()
		self.__image = Image()
		self.__menuitem1 = self.__editor.create_menuitem(_("_Tabs to Spaces (alt+shift+t)"))
		self.__menuitem2 = self.__editor.create_menuitem(_("_Spaces to Tabs (alt+t)"))
		self.__menuitem3 = self.__editor.create_menuitem(_("_Remove Trailing Spaces (alt+r)"))
		return

	def __set_properties(self):
		self.set_property("name", "Spaces Popup Menuitem")
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		if self.__editor.readonly: self.set_property("sensitive", False)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("tabs-to-spaces")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("spaces-to-tabs")
		else:
			self.__editor.trigger("remove-trailing-spaces")
		return True

	def __destroy_cb(self, *args):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__view)
		self.destroy()
		del self
		self = None
		return False
