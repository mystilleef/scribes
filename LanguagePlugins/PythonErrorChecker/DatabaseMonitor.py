from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		_file = join(editor.metadata_folder, "PluginPreferences", "PythonErrorCheckType.gdb")
		self.__monitor = editor.get_file_monitor(_file)
		return

	def __update(self):
		self.__manager.emit("database-updated")
		return False

	def __update_timeout(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__update, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.__monitor.cancel()
		self.disconnect()
		del self
		return False

	def __update_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		try:
			from gobject import timeout_add, source_remove, PRIORITY_LOW
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(250, self.__update_timeout, priority=PRIORITY_LOW)
		return False
