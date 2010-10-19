class Listener(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__update_cb)
		self.__update()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(self.__get_path()).monitor_file(FILE_MONITOR_NONE, None)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __get_path(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "PluginPreferences")
		return join(folder, "TemplateIndentation.gdb")

	def __update(self):
		from Metadata import get_value
		self.__manager.emit("get-data", get_value())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		monitor, gfile, otherfile, event = args
		if not (event in (0,2,3)): return False
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False
