class Generator(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("schemes", self.__schemes_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __send_treeview_data(self, schemes):
		can_remove = lambda scheme: scheme.get_filename().startswith(self.__editor.home_folder)
		get_description = lambda scheme: (scheme.get_name() + " - " + scheme.get_description())
		format = lambda scheme: (get_description(scheme), scheme, can_remove(scheme))
		data = [format(scheme) for scheme in schemes]
		self.__manager.emit("treeview-data", data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __schemes_cb(self, manager, schemes):
		self.__send_treeview_data(schemes)
		return False
