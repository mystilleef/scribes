class Manager(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sig_id1 = manager.connect("destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__changed_cb)
		self.__send_show_signal()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "PluginPreferences")
		database_path = join(preference_folder, "DrawWhitespace.gdb")
		self.__monitor = editor.get_file_monitor(database_path)
		return

	def __send_show_signal(self):
		from DrawWhitespaceMetadata import get_value
		self.__manager.emit("show", get_value())
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __changed_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		self.__send_show_signal()
		return False
