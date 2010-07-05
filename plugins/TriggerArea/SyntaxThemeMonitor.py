from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "syntax-color-theme-changed", self.__changed_cb, True)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__widget = manager.get_data("TriggerWidget")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __change_color(self):
		self.__widget.change_bg_color()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__change_color)
		return False
