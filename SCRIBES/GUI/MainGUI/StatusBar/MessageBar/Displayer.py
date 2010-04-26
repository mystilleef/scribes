from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "bar", self.__bar_cb)
		self.connect(manager, "_hide", self.__hide_cb)
		self.connect(manager, "_show", self.__show_cb)
		self.connect(manager, "visible", self.__visible_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		self.__visible = False
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __hide(self):
		self.__editor.response()
		self.__manager.emit("slide", "down")
		self.__editor.response()
		return False

	def __show(self):
		self.__bar.queue_resize()
		self.__editor.response()
		self.__manager.emit("slide", "left")
		self.__editor.response()
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __visible_cb(self, manager, visible):
		if visible is False: self.__bar.queue_resize()
		return False
