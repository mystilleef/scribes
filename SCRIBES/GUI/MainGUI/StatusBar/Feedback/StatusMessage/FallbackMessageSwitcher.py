from gettext import gettext as _

class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("fallback", self.__fallback_cb)
		self.__sigid3 = manager.connect("busy", self.__busy_cb)
		self.__sigid4 = editor.connect("loaded-file", self.__loaded_cb)
		self.__sigid5 = editor.connect("renamed-file", self.__loaded_cb)
		self.__sigid6 = editor.connect("saved-file", self.__saved_cb)
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
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __fallback(self):
		try:
			if self.__busy: return False
			emit = lambda message, bold, italic: self.__manager.emit("fallback-message", message, bold, italic, "")
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
		from gio import File
		filename = File(uri).get_parse_name()
		return filename.replace(self.__editor.home_folder.rstrip("/"), "~")

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fallback_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(300, self.__fallback, priority=99999)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False

	def __loaded_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__generate_names, uri)
		return False

	def __saved_cb(self, editor, uri, *args):
		if editor.generate_filename is False: return False
		from gobject import idle_add
		idle_add(self.__generate_names, uri)
		return False
