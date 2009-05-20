class Listener(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__update_cb)
		self.__update()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__monitor = editor.get_file_monitor(self.__get_path())
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__monitor.cancel()
		del self
		self = None
		return False

	def __get_path(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "PluginPreferences")
		return join(folder, "TemplateIndentation.gdb")

	def __update(self):
		from TemplateIndentationMetadata import get_value
		self.__manager.emit("reformat-template", get_value())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False
