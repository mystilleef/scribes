from gettext import gettext as _
from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		editor.response()
		ImageMenuItem.__init__(self, _("Bookmark"))
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__menuitem1.connect("map-event", self.__map_cb)
		self.__sigid5 = self.__menuitem2.connect("map-event", self.__map_cb)
		self.__sigid6 = self.__menuitem3.connect("map-event", self.__map_cb)
		self.__sigid7 = editor.textview.connect("focus-in-event", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import Menu
		self.__menu = Menu()
		from os.path import join
		current_folder = self.__editor.get_current_folder(globals())
		image = join(current_folder, "bookmarks.png")
		self.__image = self.__editor.create_image(image)
		self.__menuitem1 = self.__editor.create_menuitem(_("_Toggle Bookmark (ctrl + d)"))
		self.__menuitem2 = self.__editor.create_menuitem(_("_Remove All Bookmarks (ctrl + shift + b)"))
		self.__menuitem3 = self.__editor.create_menuitem(_("_Show Bookmark Browser (ctrl + b)"))
		return

	def __set_properties(self):
		self.set_property("name", "Bookmarks Popup Menuitem")
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("toggle-bookmark")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("remove-all-bookmarks")
		else:
			self.__editor.trigger("show-bookmark-browser")
		return False

	def __map_cb(self, menuitem, event):
		self.__sensitize_menuitem(menuitem)
		return False

	def __sensitize_menuitem(self, menuitem):
		if menuitem in (self.__menuitem2, self.__menuitem3):
			menuitem.set_property("sensitive", self.__editor.textview.get_show_line_marks())
		else:
			menuitem.set_property("sensitive", True)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid5, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid6, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor.textview)
		self.__menuitem1.destroy()
		self.__menuitem2.destroy()
		self.__menuitem3.destroy()
		self.__menu.destroy()
		self.__image.destroy()
		self.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
