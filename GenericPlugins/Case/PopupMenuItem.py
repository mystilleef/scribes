from gettext import gettext as _
from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		ImageMenuItem.__init__(self, _("_Case"))
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__menuitem1.connect("map-event", self.__map_event_cb)
		self.__sigid5 = self.__menuitem2.connect("map-event", self.__map_event_cb)
		self.__sigid6 = self.__menuitem3.connect("map-event", self.__map_event_cb)
		self.__sigid7 = self.__editor.textview.connect("focus-in-event", self.__focus_cb)

	def __init_attributes(self, editor):
		from gtk import Menu, Image, STOCK_SORT_DESCENDING
		self.__image = Image()
		self.__image.set_property("stock", STOCK_SORT_DESCENDING)
		self.__editor = editor
		self.__menu = Menu()
		self.__menuitem1 = editor.create_menuitem(_("_Togglecase (alt + u)"))
		self.__menuitem2 = editor.create_menuitem(_("_Titlecase (alt + shift + u)"))
		self.__menuitem3 = editor.create_menuitem(_("_Swapcase  (alt + shift + l)"))
		return

	def __set_properties(self):
		self.set_property("name", "Case Popup MenuItem")
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		if self.__editor.readonly: self.set_property("sensitive", False)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("togglecase")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("titlecase")
		else:
			self.__editor.trigger("swapcase")
		return True

	def __map_event_cb(self, menuitem, event):
		return False

	def __focus_cb(self, textview, event):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid5, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid6, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor.textview)
		self.__menu.destroy()
		self.__image.destroy()
		self.destroy()
		del self
		self = None
		return False
