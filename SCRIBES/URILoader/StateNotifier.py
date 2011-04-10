class Notifier(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("init-loading", self.__init_loading_cb)
		self.__sigid3 = manager.connect("error", self.__error_cb)
		self.__sigid4 = manager.connect("read-uri", self.__read_uri_cb)
		self.__sigid5 = manager.connect("encoding-error", self.__encoding_error_cb)
		self.__sigid6 = manager.connect("load-success", self.__load_success_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __init_loading_cb(self, manager, uri, encoding):
		from gobject import idle_add
		idle_add(self.__editor.emit, "checking-file", uri)
		return False

	def __error_cb(self, manager, uri, error_code):
		from gobject import idle_add
		idle_add(self.__editor.emit, "load-error", uri)
		return False

	def __read_uri_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__editor.emit, "loading-file", uri)
		return False

	def __encoding_error_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__editor.emit, "load-error", uri)
		return False

	def __load_success_cb(self, manager, uri, encoding):
		from gobject import idle_add
		idle_add(self.__editor.emit, "loaded-file", uri, encoding)
		return False
