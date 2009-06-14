class Updater(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("loaded-file", self.__encoding_cb)
		self.__sigid2 = editor.connect("saved-file", self.__update_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__update_cb)
		self.__sigid4 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__encoding = "utf-8"
		return

	def __update(self, uri, encoding):
		encoding = self.__manager.format_encoding(encoding)
		if encoding == self.__encoding: return False
		from FileEncodingsMetadata import set_value
		set_value(uri, encoding)
		return False

	def __update_encoding(self, uri):
		from FileEncodingsMetadata import get_value
		self.__encoding = get_value(uri)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__update, uri, encoding)
		return False

	def __encoding_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__update_encoding, uri)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
