class Updater(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("loaded-file", self.__update_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__update_cb)
		self.__sigid4 = editor.connect("update-encoding-guess-list", self.__update_cb)
		editor.response()
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
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

	def __update(self, encoding):
		encoding = self.__manager.format_encoding(encoding)
		from EncodingGuessListMetadata import set_value
		set_value(encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, args[-1])
		return False