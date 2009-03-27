from gettext import gettext as _

class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("fallback", self.__fallback_cb)
		self.__sigid3 = manager.connect("busy", self.__busy_cb)
		self.__sigid4 = editor.connect("loaded-file", self.__loaded_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		self.__normal_filename = ""
		self.__modified_filename = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __fallback(self):
		try:
			if self.__busy: return False
			emit = lambda message, bold, italic: self.__manager.emit("update-message", message, bold, italic, "")
			if not self.__editor.uri: raise ValueError
			mname, nname = self.__modified_filename, self.__normal_filename
			emit(mname, False, True) if self.__editor.modified else emit(nname, True, False)
		except ValueError:
			emit("", False, False)
		return False

	def __generate_names(self, uri):
		filename = self.__get_filename(uri)
		self.__modified_filename = filename + _(" [modified]")
		self.__normal_filename = filename
		return False

	def __get_filename(self, uri):
		from gnomevfs import URI, unescape_string_for_display
		filename = str(URI(uri).path)
		filename = filename.replace(self.__editor.home_folder.rstrip("/"), "~")
		return unescape_string_for_display(filename)

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fallback_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__fallback, priority=9999)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False

	def __loaded_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__generate_names, uri)
		return False