class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("database-update", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 

	def __update(self):
		from Metadata import get_value
		self.__manager.emit("dictionary", get_value())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		self.__update()
		return False
