from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(editor, "freeze", self.__freeze_cb)
		self.connect(editor, "thaw", self.__thaw_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__is_frozen = 0
		return

	def __freeze_cb(self, *args):
		try:
			if self.__is_frozen: raise ValueError
			from sys import setcheckinterval
			setcheckinterval(1000)
			self.__view.set_editable(False)
			self.__view.window.freeze_updates()
		except ValueError:
			pass
		finally:
			self.__is_frozen += 1
		return False

	def __thaw_cb(self, *args):
		try:
			if not self.__is_frozen: raise ValueError
			self.__view.set_editable(True)
			from sys import setcheckinterval
			setcheckinterval(-1)
			self.__view.window.thaw_updates()
		except ValueError:
			pass
		finally:
			self.__is_frozen -= 1
			if self.__is_frozen < 0: self.__is_frozen = 0
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
