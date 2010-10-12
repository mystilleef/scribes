class Generator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__emit_model_data()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __emit_model_data(self):
		language_list = self.__editor.language_objects
		data = [(name.get_name(), name.get_id()) for name in language_list]
		data.insert(0, ("General", "General"))
		self.__manager.emit("language-treeview-data", data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
