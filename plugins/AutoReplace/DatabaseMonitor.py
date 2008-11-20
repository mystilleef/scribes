class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from os.path import join
		path_ = join(editor.metadata_folder, "abbreviations.gdb")
		from gnomevfs import get_uri_from_local_path as path_to_uri
		self.__uri = path_to_uri(path_)
		return  

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return 

	def __update(self, *args):
		self.__manager.emit("database-update")
		return False
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		self.__update()
		return False
