class Initializer(object):

	def __init__(self, manager, editor, uri, encoding):
		editor.response()
		self.__init_attibutes(manager, editor)
		self.__sigid1 = editor.connect("load-file", self.__load_file_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		if uri: editor.load_file(uri, encoding)
		editor.response()

	def __init_attibutes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __load(self, uri, encoding):
		self.__manager.emit("init-loading", uri, encoding)
		self.__manager.emit("check-file-type", uri)
		return False

	def __load_file_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__load, uri, encoding)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
