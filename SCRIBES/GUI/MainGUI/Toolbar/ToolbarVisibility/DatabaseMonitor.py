class Monitor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("database-query", self.__changed_cb)
		self.__monitor.connect("changed", self.__changed_cb)
		manager.emit("database-query")
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(self.__get_path()).monitor_file(FILE_MONITOR_NONE, None)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __get_path(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "Preferences")
		return join(folder, "MinimalMode.gdb")

	def __emit(self):
		from SCRIBES.MinimalModeMetadata import get_value as minimal_mode
		self.__manager.emit("minimal-mode", minimal_mode())
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		try:
			monitor, gfile, otherfile, event = args
			if not (event in (0,2,3)): return False
		except ValueError:
			pass
		from gobject import idle_add
		idle_add(self.__emit, priority=9999)
		return False
