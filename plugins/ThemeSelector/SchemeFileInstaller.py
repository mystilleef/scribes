class Installer(object):

	def __init__(self, editor, manager):
		editor.response()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("valid-scheme-files", self.__valid_cb)
		editor.response()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
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
		folder = join(self.__editor.home_folder, ".gnome2", "scribes", "styles")
		if not exists(folder): makedirs(folder)
		return folder

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __valid_cb(self, manager, filenames):
		from gobject import idle_add
		idle_add(self.__install, filenames)
		return False
