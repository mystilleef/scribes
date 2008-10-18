from gtk import Menu

class PopupMenu(Menu):
	
	def __init__(self, manager, editor):
		Menu.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("popup-menu", self.__popup_menu_cb)
		self.__sigid3 = manager.connect("hide-menu", self.__hide_menu_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("MenuButton")
		self.__hbox = manager.gui.get_widget("HBox")
		return 
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return
	
	def __set_properties(self):
		from gtk import MenuItem
		self.append(MenuItem("Match _Case"))
		self.append(MenuItem("Match _Word"))
		self.append(MenuItem("_Normal"))
		self.append(MenuItem("F_orward"))
		self.append(MenuItem("B_ackward"))
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __hide_menu_cb(self, *args):
		self.hide()
		return False

	def __popup_menu_cb(self, manager, data):
		self.popup(None, None, None, *data)
		self.show_all()
		return False
