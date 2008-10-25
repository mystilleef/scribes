class PopupMenu(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("popup-menu", self.__popup_menu_cb)
		self.__sigid3 = manager.connect("hide-menu", self.__hide_menu_cb)
		self.__sigid4 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid5 = manager.connect("hide-bar", self.__hide_menu_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("MenuButton")
		self.__container = manager.gui.get_widget("Table")
		self.__window = manager.menu_gui.get_widget("MenuWindow")
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __hide_menu_cb(self, *args):
		self.__hide()
		return False

	def __position(self):
		winx, winy = self.__editor.window.window.get_origin()
		hbox_y = winy + self.__container.allocation.y
		hbox_x = winx + self.__button.allocation.x
		y = hbox_y - self.__window.size_request()[1]
		self.__window.move(hbox_x, y)
		return

	def __hide(self):
		self.__window.hide()
		return 

	def __show(self):
		self.__position()
		self.__window.show_all()
		return 

	def __popup_menu_cb(self, *args):
		self.__show()
		return False

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide-menu")
		return True
