class Loader(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("open-encoding", self.__encoding_cb)
		self.__sigid3 = manager.connect("load-files", self.__load_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.open_gui.get_object("FileChooser")
		self.__encoding = ""
		return

	def __load_uris(self, uris):
		self.__editor.response()
		encoding = self.__encoding if self.__encoding else "utf8"
		self.__editor.response()
		self.__manager.emit("open-files", uris, encoding)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __load_cb(self, manager, uris):
		from gobject import idle_add
		idle_add(self.__load_uris, uris)
		return False

	def __encoding_cb(self, manager, encoding):
		self.__encoding = encoding
		return False
