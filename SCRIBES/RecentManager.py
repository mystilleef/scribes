from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "loaded-file", self.__loaded_file_cb)
		self.connect(editor, "renamed-file", self.__renamed_file_cb)
		editor.set_data("RecentManager", self.__manager)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = self.__create_recent_manager()
		return

	def __create_recent_manager(self):
		from gtk import recent_manager_get_default
		manager = recent_manager_get_default()
		return manager

	def __create_recent_data(self, uri):
		fileinfo = self.__editor.get_fileinfo(uri)
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
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
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
