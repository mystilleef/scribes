from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "execute", self.__freeze_cb)
		self.connect(manager, "restored-cursor-position", self.__thaw_cb, True)
		self.connect(manager, "output-mode", self.__output_cb, True)
		self.connect(manager, "win", self.__win_cb, True)
		self.connect(manager, "fail", self.__thaw_cb, True)
		self.connect(manager, "hide", self.__thaw_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__frozen = False
		self.__output_mode = "replace"
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __freeze(self):
		if self.__frozen: return False
		self.__editor.freeze()
		self.__frozen = True
		return False

	def __thaw(self):
		if self.__frozen is False: return False
		self.__editor.thaw()
		self.__frozen = False
		return False

	def __freeze_cb(self, *args):
		self.__freeze()
		return False

	def __thaw_cb(self, *args):
		self.__thaw()
		return False

	def __win_cb(self, *args):
		if self.__output_mode == "replace": return False
		self.__thaw()
		return False

	def __output_cb(self, manager, output):
		self.__output_mode = output
		return False
