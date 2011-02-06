from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(editor, "load-file", self.__freeze_cb)
		self.connect(editor, "loaded-file", self.__thaw_cb, True)
		self.connect(editor, "load-error", self.__thaw_cb)
		editor.register_object(self)

	def __destroy_cb(self, editor, *args):
		self.disconnect()
		editor.unregister_object(self)
		del self
		return False

	def __freeze_cb(self, editor, *args):
		editor.window.window.freeze_updates()
		editor.freeze()
		return False

	def __thaw_cb(self, editor, *args):
		editor.thaw()
		editor.window.window.thaw_updates()
		return False
