class Manager(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sig_id1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__send_show_signal()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "PluginPreferences")
		database_path = join(preference_folder, "DrawWhitespace.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__sig_id1 = self.__monitor_id_1 = None
		return

	def __send_show_signal(self):
		from DrawWhitespaceMetadata import get_value
		self.__manager.emit("show", get_value())
		return

	def __destroy(self):
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __database_changed_cb(self, *args):
		self.__send_show_signal()
		return False
