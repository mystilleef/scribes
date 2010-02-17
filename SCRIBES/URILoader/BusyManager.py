class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("init-loading", self.__busy_cb)
		self.__sigid3 = manager.connect("error", self.__nobusy_cb)
		self.__sigid4 = manager.connect("encoding-error", self.__nobusy_cb)
		self.__sigid5 = manager.connect("load-success", self.__nobusy_cb)
		self.__sigid6 = editor.connect("load-error", self.__nobusy_cb)
		editor.response()
#		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		signals = (
			(self.__sigid1, self.__manager),
			(self.__sigid2, self.__manager),
			(self.__sigid3, self.__manager),
			(self.__sigid4, self.__manager),
			(self.__sigid5, self.__manager),
			(self.__sigid6, self.__editor),
		)
		self.__editor.disconnect_signals(signals)
#		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, *args):
		self.__editor.busy()
		return False

	def __nobusy_cb(self, *args):
		self.__editor.busy(False)
		return False
