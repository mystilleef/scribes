class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__database_changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Path to the templates database.
		database_path = editor.metadata_folder + "templates.gdb"
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __database_changed_cb(self, *args):
		self.__manager.emit("database-updated")
		return False
