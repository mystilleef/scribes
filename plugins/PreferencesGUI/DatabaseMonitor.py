class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences", "Languages")
		self.__monitor = editor.get_folder_monitor(preference_folder)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		self.__manager.emit("database-update")
		return False
