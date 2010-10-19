class Creator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("create-export-template-filename", self.__create_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __create(self, filename):
		open(filename, "w").close()
		self.__manager.emit("created-template-file")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __create_cb(self, manager, filename):
		self.__create(filename)
		return False
