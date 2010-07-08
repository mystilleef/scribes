from SCRIBES.SignalConnectionManager import SignalManager

class Quiter(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.__sigid1 = self.connect(self.__window, "key-press-event", self.__event_cb)
		self.__block()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = editor.window
		self.__blocked = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __deactivate(self):
		self.__block()
		self.__manager.emit("deactivate")
		return False

	def __block(self):
		if self.__blocked: return False
		self.__window.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__window.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		self.__unblock()
		return False

	def __event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__deactivate()
		return True
