class Notifier(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("init-loading", self.__init_loading_cb)
		self.__sigid3 = manager.connect("error", self.__error_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

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

	def __init_loading_cb(self, manager, uri, encoding):
		self.__editor.emit("checking-file", uri)
		return False

	def __error_cb(self, manager, uri, error_code):
		self.__editor.emit("load-error", uri)
		return False
