class Selector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("toggled-path", self.__path_cb)
		self.__sigid3 = manager.connect("updated-model", self.__updated_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_widget("TreeView")
		self.__model = self.__view.get_model()
		self.__column = self.__view.get_column(0)
		self.__path = 0
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __select(self):
		self.__view.set_cursor(self.__path, self.__column)
		self.__path = 0
		self.__view.set_property("sensitive", True)
		self.__view.grab_focus()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __path_cb(self, manager, path):
		self.__path = path
		return False

	def __updated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__select)
		return False
