class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from os.path import join
		folder = join(editor.metadata_folder, "PluginPreferences")
		filepath = join(folder, "Templates.gdb")
		from gnomevfs import get_uri_from_local_path as get_uri
		self.__uri = get_uri(filepath)
		return

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__manager.emit("database-update")
		return False
