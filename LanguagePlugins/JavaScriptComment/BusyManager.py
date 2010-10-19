from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb, True)
		self.connect(manager, "finished", self.__finished_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
#		self.__editor.busy(True)
		self.__editor.textview.window.freeze_updates()
		return False

	def __finished_cb(self, *args):
		self.__editor.textview.window.thaw_updates()
#		self.__editor.busy(False)
		return False
