from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "message-bar-is-updated", self.__update_cb, True)
		self.connect(manager, "reset", self.__fallback_cb, True)
		self.connect(manager, "fallback", self.__fallback_cb, True)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bar = editor.get_data("MessageBar")
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __hide(self):
		self.__bar.hide()
		return False

	def __show(self):
		self.__bar.show()
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __show_on_idle(self):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__show, priority=PRIORITY_LOW)
		return False

	def __update_cb(self, manager, data):
		self.__remove_timer()
		self.__hide()
		show_bar = data[-1]
		if not show_bar: return False
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(150, self.__show_on_idle, priority=PRIORITY_LOW)
		return False

	def __fallback_cb(self, *args):
		self.__remove_timer()
		self.__hide()
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__hide, priority=PRIORITY_LOW)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
