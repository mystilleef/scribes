from gtk import ImageMenuItem
from gettext import gettext as _

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		ImageMenuItem.__init__(self, _("In_dentation"))
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__textview.connect("focus-in-event", self.__focus_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import STOCK_INDENT, STOCK_UNINDENT, Image, Menu
		self.__image = Image()
		self.__menu = Menu()
		self.__textview = editor.textview
		self.__menuitem1 = editor.create_menuitem(_("Shift _Right"), STOCK_INDENT)
		self.__menuitem2 = editor.create_menuitem(_("Shift _Left"), STOCK_UNINDENT)
		return

	def __set_properties(self):
		self.set_property("name", "Indentation Popup MenuItem")
		from gtk import STOCK_JUSTIFY_CENTER
		self.__image.set_property("stock", STOCK_JUSTIFY_CENTER)
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		if self.__editor.readonly: self.set_property("sensitive", False)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("indent")
		else:
			self.__editor.trigger("unindent")
		return True

	def __focus_cb(self, *args):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid3, self.__textview)
		self.destroy()
		del self
		self = None
		return False
