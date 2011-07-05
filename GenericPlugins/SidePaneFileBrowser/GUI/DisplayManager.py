from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__container = manager.gui.get_object("BrowserContainer1")
		self.__treeview = manager.gui.get_object("TreeView")
		self.__side_pane =  editor.gui.get_widget("SidePane")
		return

	def __hide(self):
		self.__side_pane.hide()
		self.__container.hide()
		from gobject import idle_add
		idle_add(self.__manager.emit, "hiding-browser")
		self.__treeview.columns_autosize()
		return False

	def __show(self):
		self.__side_pane.show_all()
		self.__container.show_all()
		from gobject import idle_add
		idle_add(self.__manager.emit, "showing-browser")
		self.__treeview.columns_autosize()
		return False

	def __activate(self):
		is_visible = self.__container.get_property("visible")
		from gobject import idle_add
		idle_add(self.__hide) if is_visible else idle_add(self.__show)
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
