from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		editor.set_data("completion_window_is_visible", False)
		self.connect(editor, "completion-window-is-visible", self.__visible_cb)
		self.connect(editor, "quit", self.__quit_cb)

	def __visible_cb(self, editor, visible):
		editor.set_data("completion_window_is_visible", visible)
		return False

	def __quit_cb(self, *args):
		self.disconnect()
		del self
		return False
