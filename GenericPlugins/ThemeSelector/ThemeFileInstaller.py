from SCRIBES.SignalConnectionManager import SignalManager

class Installer(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "valid-scheme-files", self.__valid_cb)
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __install(self, filenames):
		from shutil import copy
		folder = self.__get_scheme_folder()
		copy_ = lambda filename: copy(filename, folder)
		[copy_(_file) for _file in filenames]
		return False

	def __get_scheme_folder(self):
		from os.path import join, exists
		from os import makedirs
		folder = join(self.__editor.metadata_folder, "styles")
		if not exists(folder): makedirs(folder)
		return folder

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __valid_cb(self, manager, filenames):
		from gobject import idle_add
		idle_add(self.__install, filenames)
		return False
