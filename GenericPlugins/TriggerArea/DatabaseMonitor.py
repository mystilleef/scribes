from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		folder = join(editor.metadata_folder, "PluginPreferences", "TriggerArea")
		self.__monitor = editor.get_folder_monitor(folder)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.disconnect()
		del self
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		self.__manager.emit("database-update")
		return False
