from SCRIBES.SignalConnectionManager import SignalManager

SAVE_TIMER = 3000

class Saver(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.__sigid1 = self.connect(editor, "modified-file", self.__modified_cb)
		self.connect(editor, "close", self.__close_cb)
		self.connect(editor, "cursor-moved", self.__changed_cb, True)
		self.connect(editor.buf, "changed", self.__changed_cb, True)
		self.connect(manager, "reset-modification-flag", self.__modified_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__remove_timer()
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
				3: self.__timer3,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 4)]
		return False

	def __process(self):
		self.__remove_all_timers()
		from gobject import timeout_add as ta, PRIORITY_LOW
		self.__timer1 = ta(SAVE_TIMER, self.__save_on_idle, priority=PRIORITY_LOW)
		return False

	def __save_on_idle(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__save, priority=PRIORITY_LOW)
		return False

	def __save(self):
		if self.__editor.modified is False: return False
		self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __close_cb(self, *args):
		self.__remove_all_timers()
		self.__editor.handler_block(self.__sigid1)
		return False

	def __modified_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer3 = idle_add(self.__process, priority=PRIORITY_LOW)
		return False

	def __changed_cb(self, *args):
		self.__process()
		return False
