from gettext import gettext as _

class Updater(object):

	def __init__(self, editor, uri):
		editor.response()
		self.__init_attributes(editor, uri)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__checking_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__loaded_cb)
		self.__sigid4 = editor.connect("load-error", self.__error_cb)
		self.__sigid5 = editor.connect_after("modified-file", self.__modified_cb)
		self.__sigid6 = editor.connect("readonly", self.__readonly_cb)
		self.__sigid7 = editor.connect("saved-file", self.__saved_cb)
		if uri: self.__set_title("loading")
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.window
		self.__uri = uri
		self.__dictionary = self.__get_dictionary(uri)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update_attributes(self, uri):
		self.__uri = uri
		self.__dictionary = self.__get_dictionary(uri)
		return False

	def __get_dictionary(self, uri):
		from gio import File
		title = File(uri).get_basename() if uri else _("Unsaved Document")
		dictionary = {
			"normal": title,
			"modified": "*" + title,
			"readonly": title + _(" [READONLY]"),
			"loading": _("Loading %s ...") % title,
		}
		return dictionary

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
