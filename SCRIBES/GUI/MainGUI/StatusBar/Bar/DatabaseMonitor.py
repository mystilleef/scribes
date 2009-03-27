class Monitor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("database-query", self.__changed_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		manager.emit("database-query")
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__uri = self.__get_database_uri()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __get_database_uri(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "Preferences")
		filepath = join(folder, "MinimalMode.gdb")
		from gnomevfs import get_uri_from_local_path as get_uri
		return get_uri(filepath)

	def __emit(self):
		from SCRIBES.MinimalModeMetadata import get_value as minimal_mode
		self.__manager.emit("minimal-mode", minimal_mode())
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__emit, priority=9999)
		return False
