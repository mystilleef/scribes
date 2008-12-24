class Monitor(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		# Monitor database for changes.
		from gnomevfs import monitor_add, MONITOR_DIRECTORY as FOLDER
		self.__monid1 = monitor_add(self.__uri1, FOLDER, self.__changed_cb)
		self.__monid2 = monitor_add(self.__uri2, FOLDER, self.__changed_cb)
		self.__monid3 = monitor_add(self.__uri3, FOLDER, self.__changed_cb)
		self.__scan()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		scribes_path = join(self.__editor.home_folder, ".gnome2/scribes/styles")
		gedit_path = join(self.__editor.home_folder, ".gnome2/gedit/styles")
		default_path = join(self.__editor.home_folder, ".local/share/gtksourceview-2.0/styles")
		from gnomevfs import get_uri_from_local_path
		self.__uri1 = get_uri_from_local_path(scribes_path)
		self.__uri2 = get_uri_from_local_path(gedit_path)
		self.__uri3 = get_uri_from_local_path(default_path)
		return

	def __scan(self):
		self.__manager.emit("scan-schemes")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		monitor_cancel(self.__monid2)
		monitor_cancel(self.__monid3)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __changed_cb(self, *args):
		self.__scan()
		return True
