class Manager(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		self.__send_activate_signal()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "UseTabs.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__uri = get_uri_from_local_path(database_path)
		return

	def __send_activate_signal(self):
		use_spaces = self.__editor.textview.get_insert_spaces_instead_of_tabs()
		self.__manager.emit("activate", use_spaces)
		return False

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __changed_cb(self, *args):
		from gobject import timeout_add
		timeout_add(200, self.__send_activate_signal)
		return False
