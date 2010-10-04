class Selector(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("new-template-data", self.__data_cb)
		self.__sigid3 = manager.connect("populated-description-treeview", self.__populated_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__key = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __emit_description_treeview_selection(self):
		self.__manager.emit("select-description-treeview", self.__key)
		self.__key = ""
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		self.__key = data[1]
		return False

	def __populated_cb(self, *args):
		self.__emit_description_treeview_selection()
		return False
