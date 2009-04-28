class Listener(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__update_cb)
		self.__update()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__uri = self.__get_uri()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		del self
		self = None
		return False

	def __get_uri(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "PluginPreferences")
		_path = join(folder, "TemplateIndentation.gdb")
		from gnomevfs import get_uri_from_local_path as get_uri
		return get_uri(_path)

	def __update(self):
		from Metadata import get_value
		self.__manager.emit("get-data", get_value())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False
