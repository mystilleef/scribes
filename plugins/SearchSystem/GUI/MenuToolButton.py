from gtk import MenuToolButton

class ToolButton(MenuToolButton):

	def __init__(self, manager, editor):
		editor.response()
		from gtk import STOCK_PROPERTIES
		MenuToolButton.__init__(self, STOCK_PROPERTIES)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.connect("clicked", self.__clicked_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.destroy()
		del self
		self = None
		return 
	
	def __set_properties(self):
		hbox = self.__manager.gui.get_widget("HBox")
		hbox.add(self)
		hbox.reorder_child(self, 5)
		from gtk import PACK_START
		hbox.set_child_packing(self, False, False, 5, PACK_START)
		from gtk import Menu 
		self.set_menu(Menu())
		self.show_all()
		return 
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __clicked_cb(self, *args):
		self.get_menu().activate()
		return False
