from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(self.__buffer, "changed", self.__response_cb, True)
		self.connect(editor, "quit", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__is_blocked = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __response_cb(self, *args):
		self.__remove_timer(1)
		from gobject import idle_add, PRIORITY_HIGH
		self.__timer1 = idle_add(self.__editor.refresh, priority=PRIORITY_HIGH)
		return False
