class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.textview.connect_after("populate-popup", self.__popup_cb)
		self.__sigid3 = editor.connect("add-to-popup", self.__add_to_popup_cb)
		self.__sigid4 = editor.textview.connect("focus-in-event", self.__focus_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__menu = None
		self.__items = []
		return

	def __sort_items(self, menuitem):
		self.__items.append(menuitem)
		items = [(menuitem.props.name, menuitem) for menuitem in self.__items]
		items.sort()
		items.reverse()
		self.__items = [menuitem[1] for menuitem in items]
		return False

	def __generate_menu(self, menu):
		if not self.__items: return False
		from gtk import SeparatorMenuItem
		menu.insert(SeparatorMenuItem(), 0)
		for menuitem in self.__items:
			if menuitem.props.name == "AboutMenuitem":
				menu.append(SeparatorMenuItem())
				menu.append(menuitem)
				menuitem.show()
			else:
				menu.prepend(menuitem)
				menuitem.show()
		menu.show_all()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor.textview)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __popup_cb(self, textview, menu):
		self.__generate_menu(menu)
		return True

	def __add_to_popup_cb(self, editor, menuitem):
		self.__sort_items(menuitem)
		return False

	def __focus_cb(self, *args):
		self.__items = []
		return False
