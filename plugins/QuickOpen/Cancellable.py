from gio import Cancellable

class GCancellable(Cancellable):

	def __init__(self, manager, editor):
		Cancellable.__init__(self)
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("enumeration-error", self.__error_cb)
		self.__sigid3 = manager.connect("hide", self.__error_cb)

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

	def __error_cb(self, *args):
		self.cancel()
		self.reset()
		return False
