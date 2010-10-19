class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from os.path import join
		folder = join(editor.metadata_folder, "PluginPreferences")
		filepath = join(folder, "Templates.gdb")
		self.__monitor = editor.get_file_monitor(filepath)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		self.__manager.emit("database-update")
		return False
