class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid3 = self.__editor.connect("renamed-file", self.__renamed_file_cb)
		editor.set_data("RecentManager", self.__manager)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = self.__create_recent_manager()
		return

	def __create_recent_manager(self):
		from gtk import recent_manager_get_default
		manager = recent_manager_get_default()
		return manager

	def __create_recent_data(self, uri):
		from gio import File
		fileinfo = File(uri).query_info("*")
		app_name = "scribes"
		app_exec = "%U"
		description = "A text file."
		recent_data = {
			"mime_type": fileinfo.get_content_type(),
			"app_name": app_name,
			"app_exec": app_exec,
			"display_name": fileinfo.get_display_name(),
			"description": description,
		}
		return recent_data

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __loaded_file_cb(self, editor, uri, *args):
		self.__manager.add_full(uri, self.__create_recent_data(uri))
		return

	def __renamed_file_cb(self, editor, uri, *args):
		self.__manager.add_full(uri, self.__create_recent_data(uri))
		return

	def __quit_cb(self, editor):
		self.__destroy()
		return
