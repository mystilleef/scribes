class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("ready", self.__update_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__update_cb)
		self.__sigid4 = editor.connect("renamed-file", self.__update_cb)
		self.__set()
		self.__update_search_path()
		self.__editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtksourceview2 import style_scheme_manager_get_default
		self.__manager = style_scheme_manager_get_default()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self):
		self.__editor.set_data("style_scheme_manager", self.__manager)
		return False

	def __get_style_path(self, base_path):
		from os.path import join, exists
		path_ = join(self.__editor.home_folder, base_path)
		return path_ if exists(path_) else None

	def __update_search_path(self):
		gedit_path = self.__get_style_path(".gnome2/gedit/styles")
		scribes_path = self.__get_style_path(".gnome2/scribes/styles")
		search_paths = self.__manager.get_search_path()
		if gedit_path and not (gedit_path in search_paths): self.__manager.prepend_search_path(gedit_path)
		if scribes_path and not (scribes_path in search_paths): self.__manager.prepend_search_path(scribes_path)
		self.__editor.response()
		self.__manager.force_rescan()
		self.__editor.response()
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		self.__update_search_path()
		return False
