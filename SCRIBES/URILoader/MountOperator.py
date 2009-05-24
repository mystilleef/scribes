from gtk import MountOperation

class Operator(MountOperation):

	def __init__(self, manager, editor):
		MountOperation.__init__(self, editor.window)
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.connect("aborted", self.__aborted_cb)
		self.__sigid3 = self.connect("reply", self.__reply_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.__editor.disconnect_signal(self.__sigid3, self)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __aborted_cb(self, *args):
		return False

	def __reply_cb(self, operator, result):
		return False
