class Manager(object):

	def __init__(self, editor, menu):
		self.__init_attributes(editor, menu)
		menu.props.sensitive = False
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("add-to-pref-menu", self.__add_cb)
		self.__sigid3 = editor.connect("remove-from-pref-menu", self.__remove_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, editor, menu):
		self.__editor = editor
		self.__menu = menu
		self.__menuitems = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__menu.destroy()
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __add(self, menuitem):
		self.__menu.props.sensitive = False
		self.__menuitems.append(menuitem)
		menuitems = self.__sort(self.__menuitems)
		self.__update(menuitems)
		self.__menu.props.sensitive = True
		self.__menu.show_all()
		return False

	def __sort(self, menuitems):
		itemlist = [(menuitem.props.name, menuitem) for menuitem in menuitems]
		itemlist.sort()
		itemlist.reverse()
		menuitems = [element[1] for element in itemlist]
		return menuitems

	def __update(self, menuitems):
		[self.__menu.remove(menuitem) for menuitem in self.__menu.get_children()]
		[self.__menu.append(menuitem) for menuitem in menuitems]
		return False

	def __remove(self, menuitem):
		self.__menuitems.remove(menuitem)
		self.__menu.remove(menuitem)
		sensitive = True if self.__menu.get_children() else False
		self.__menu.props.sensitive = sensitive
		return False

	def __add_cb(self, editor, menuitem):
		self.__add(menuitem)
		return False

	def __remove_cb(self, editor, menuitem):
		self.__remove(menuitem)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
