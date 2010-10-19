from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__update_monitors(self.__get_monitors())
		self.__connect_monitors()
		from gobject import idle_add
		idle_add(self.__update)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__monitors = []
		return

	def __destroy(self):
		self.disconnect()
		self.__disconnect_monitors()
		del self
		return

	def __get_monitors(self):
		paths = [self.__editor.scribes_theme_folder, self.__editor.default_home_theme_folder]
		get_monitor = self.__editor.get_folder_monitor
		return [get_monitor(path) for path in paths]

	def __update_monitors(self, monitors):
		self.__monitors = monitors
		return

	def __connect_monitors(self):
		[monitor.connect("changed", self.__changed_cb) for monitor in self.__monitors]
		return False

	def __disconnect_monitors(self):
		[monitor.cancel() for monitor in self.__monitors]
		return False

	def __update(self):
		self.__manager.emit("theme-folder-update")
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __changed_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__update, priority=99999)
		return True
