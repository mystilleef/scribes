from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		from i18n import msg0011
		ImageMenuItem.__init__(self, msg0011)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sig_id_1 = self.__next_item.connect("activate", self.__activate_cb)
		self.__sig_id_2 = self.__previous_item.connect("activate", self.__activate_cb)
		self.__sig_id_3 = self.__reflow_item.connect("activate", self.__activate_cb)
		self.__sig_id_4 = editor.textview.connect("focus-in-event", self.__destroy_cb)
		self.__sig_id_5 = self.__select_item.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		from gtk import Menu, Image
		self.__editor = editor
		self.__menu = Menu()
		self.__image = Image()
		from i18n import msg0012, msg0013, msg0014, msg0015
		self.__previous_item = editor.create_menuitem(msg0012)
		self.__next_item = editor.create_menuitem(msg0013)
		self.__reflow_item = editor.create_menuitem(msg0014)
		self.__select_item = editor.create_menuitem(msg0015)
		self.__sig_id_1 = self.__sig_id_2 = self.__sig_id_3 = None
		self.__sig_id_4 = self.__sig_id_5 = None
		return

	def __set_properties(self):
		from gtk import STOCK_JUMP_TO
		self.__image.set_property("stock", STOCK_JUMP_TO)
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__previous_item)
		self.__menu.append(self.__next_item)
		self.__menu.append(self.__reflow_item)
		self.__menu.append(self.__select_item)
		if self.__editor.is_readonly:
			self.__reflow_item.set_property("sensitive", False)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__previous_item:
			self.__editor.trigger("previous_paragraph")
		elif menuitem == self.__next_item:
			self.__editor.trigger("next_paragraph")
		elif menuitem == self.__select_item:
			self.__editor.trigger("select_paragraph")
		else:
			self.__editor.trigger("reflow_paragraph")
		return False

	def __destroy_cb(self, *args):
		self.__editor.disconnect_signal(self.__sig_id_1, self.__next_item)
		self.__editor.disconnect_signal(self.__sig_id_2, self.__previous_item)
		self.__editor.disconnect_signal(self.__sig_id_3, self.__reflow_item)
		self.__editor.disconnect_signal(self.__sig_id_4, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sig_id_5, self.__select_item)
		self.__next_item.destroy()
		self.__select_item.destroy()
		self.__previous_item.destroy()
		self.__reflow_item.destroy()
		self.__menu.destroy()
		self.__image.destroy()
		self.destroy()
		del self
		self = None
		return False
