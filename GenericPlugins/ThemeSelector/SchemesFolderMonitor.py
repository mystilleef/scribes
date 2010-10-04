class Monitor(object):

	def __init__(self, editor, manager):
		editor.response()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__scribes_monitor.connect("changed", self.__changed_cb)
		self.__gedit_monitor.connect("changed", self.__changed_cb)
		self.__default_monitor.connect("changed", self.__changed_cb)
		from gobject import idle_add
		idle_add(self.__scan)
		editor.response()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		scribes_path = join(self.__editor.home_folder, ".gnome2", "scribes", "styles")
		gedit_path = join(self.__editor.home_folder, ".gnome2", "gedit", "styles")
		default_path = join(self.__editor.home_folder, ".local", "share","gtksourceview-2.0", "styles")
		self.__scribes_monitor = editor.get_folder_monitor(scribes_path)
		self.__gedit_monitor = editor.get_folder_monitor(gedit_path)
		self.__default_monitor = editor.get_folder_monitor(default_path)
		return

	def __scan(self):
		self.__manager.emit("scan-schemes")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__scribes_monitor.cancel()
		self.__gedit_monitor.cancel()
		self.__default_monitor.cancel()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __changed_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		from gobject import idle_add
		idle_add(self.__scan)
		return True
