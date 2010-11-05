from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, editor, uri):
		SignalManager.__init__(self)
		self.__init_attributes(editor, uri)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "checking-file", self.__checking_cb)
		self.connect(editor, "loaded-file", self.__loaded_cb)
		self.connect(editor, "load-error", self.__error_cb)
		self.connect(editor, "modified-file", self.__modified_cb)
		self.connect(editor, "readonly", self.__readonly_cb)
		self.connect(editor, "saved-file", self.__saved_cb)
		if uri: self.__set_title("loading")
		
		editor.register_object(self)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.window
		self.__uri = uri
		self.__dictionary = self.__get_dictionary(uri)
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update_attributes(self, uri):
		self.__uri = uri
		self.__dictionary = self.__get_dictionary(uri)
		return False

	def __get_dictionary(self, uri):
		from gio import File
		title = File(uri).get_basename() if uri else _("Unnamed Document")
		ellipsize = self.__ellipsize
		if uri: parent_path = File(uri).get_parent().get_parse_name()
		if uri: parent_path = ellipsize(parent_path.replace(self.__editor.home_folder, "~").strip("/\\"))
		fulltitle = "%s - (%s)" % (title, parent_path) if uri else title
		fulltitle = title if len(title) > 30 else fulltitle
		dictionary = {
			"normal": fulltitle,
			"modified": "*" + fulltitle,
			"readonly": fulltitle + _(" [READONLY]"),
			"loading": _("Loading %s ...") % title,
		}
		return dictionary

	def __ellipsize(self, path):
		number_of_folders = 8
		from os import sep
		folder_paths = path.split(sep)
		if len (folder_paths) < number_of_folders: return path
		first_item = folder_paths[0]
		first_path = "%s%s..." % (first_item, sep) if first_item == "~" else "%s%s..." % (first_item, sep*2)
		last_paths = tuple(folder_paths[-5:])
		from os.path import join
		return join(first_path, *last_paths).strip(sep)

	def __update_title(self, uri, title):
		self.__update_attributes(uri)
		self.__set_title(title)
		return False

	def __set_title(self, title):
		self.__window.set_title(self.__dictionary[title])
		return False

	def __checking_cb(self, editor, uri):
		from gobject import idle_add
		idle_add(self.__update_title, uri, "loading")
		return False

	def __loaded_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__set_title, "normal")
		return False

	def __error_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update_title, None, "normal")
		return False

	def __readonly_cb(self, editor, readonly):
		from gobject import idle_add
		idle_add(self.__set_title, "readonly" if readonly else "normal")
		return False

	def __modified_cb(self, editor, modified):
		from gobject import idle_add
		idle_add(self.__set_title, "modified" if modified else "normal")
		return False

	def __saved_cb(self, editor, uri, *args):
		if self.__uri == uri: return False
		from gobject import idle_add
		idle_add(self.__update_title, uri, "normal")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
