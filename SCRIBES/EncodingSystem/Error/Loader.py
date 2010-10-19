class Loader(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("activate", self.__error_cb)
		self.__sigid3 = manager.connect("new-encoding", self.__encoding_cb)
		self.__sigid4 = manager.connect("load", self.__load_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__uri = ""
		self.__encoding = "utf-8"
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __load(self):
		self.__editor.load_file(self.__uri, self.__encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, manager, uri, *args):
		self.__uri = uri
		return False

	def __encoding_cb(self, editor, encoding):
		self.__encoding = encoding
		return False

	def __load_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load)
		return False
