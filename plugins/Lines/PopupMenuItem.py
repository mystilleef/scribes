from gtk import ImageMenuItem
from gettext import gettext as _

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		ImageMenuItem.__init__(self, _("_Lines"))
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__menuitem4.connect("activate", self.__activate_cb)
		self.__sigid5 = self.__menuitem5.connect("activate", self.__activate_cb)
		self.__sigid6 = self.__menuitem6.connect("activate", self.__activate_cb)
		self.__sigid7 = self.__menuitem7.connect("activate", self.__activate_cb)
		self.__sigid8 = self.__view.connect("focus-in-event", self.__destroy_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		from gtk import Menu, Image
		self.__menu = Menu()
		self.__image = Image()
		self.__menuitem1 = self.__editor.create_menuitem(_("_Join Line (alt + j)"))
		self.__menuitem2 = self.__editor.create_menuitem(_("D_uplicate Line (ctrl + shift + d)"))
		self.__menuitem3 = self.__editor.create_menuitem(_("_Delete Line (alt + d)"))
		self.__menuitem4 = self.__editor.create_menuitem(_("Free Line _Below (alt + o)"))
		self.__menuitem5 = self.__editor.create_menuitem(_("Free Line _Above (alt + shift + o)"))
		self.__menuitem6 = self.__editor.create_menuitem(_("Delete Cursor to Line _End (alt + End)"))
		self.__menuitem7 = self.__editor.create_menuitem(_("Delete _Cursor to Line Begin (alt + Home)"))
		return

	def __set_properties(self):
		self.set_property("name", "Line Operation Menuitem")
		from gtk import STOCK_JUSTIFY_CENTER
		self.__image.set_property("stock", STOCK_JUSTIFY_CENTER)
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		self.__menu.append(self.__menuitem4)
		self.__menu.append(self.__menuitem5)
		self.__menu.append(self.__menuitem6)
		self.__menu.append(self.__menuitem7)
		if self.__editor.readonly: self.set_property("sensitive", False)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("join_line")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("duplicate_line")
		elif menuitem == self.__menuitem3:
			self.__editor.trigger("delete_line")
		elif menuitem == self.__menuitem4:
			self.__editor.trigger("free_line_below")
		elif menuitem == self.__menuitem5:
			self.__editor.trigger("free_line_above")
		elif menuitem == self.__menuitem6:
			self.__editor.trigger("delete_cursor_to_end")
		elif menuitem == self.__menuitem7:
			self.__editor.trigger("delete_cursor_to_begin")
		return True

	def __destroy_cb(self, *args):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__menuitem4)
		self.__editor.disconnect_signal(self.__sigid5, self.__menuitem5)
		self.__editor.disconnect_signal(self.__sigid6, self.__menuitem6)
		self.__editor.disconnect_signal(self.__sigid7, self.__menuitem7)
		self.__editor.disconnect_signal(self.__sigid8, self.__view)
		self.destroy()
		del self
		self = None
		return False
