from gtk import MountOperation

class Operator(MountOperation):

	def __init__(self, manager, editor):
		MountOperation.__init__(self, editor.window)
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
