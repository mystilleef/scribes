from SCRIBES.SignalConnectionManager import SignalManager

class Reseter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "found-matches", self.__matches_cb)
		self.__sig1 = self.connect(self.__buffer, "changed", self.__changed_cb, True)
		self.__sig2 = self.connect(self.__window, "key-press-event", self.__key_cb)
		self.__sig3 = self.connect(self.__view, "focus-out-event", self.__changed_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__window = editor.window
		self.__view = editor.textview
		self.__can_reset = False
		self.__blocked = False
		return

	def __reset(self):
		if self.__can_reset is False: return
		self.__block()
		from gobject import idle_add
		idle_add(self.__manager.emit, "reset")
		return False

	def __reset_on_idle(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer3 = idle_add(self.__reset, priority=PRIORITY_LOW)
		return False

	def __block(self):
		if self.__blocked: return False
		self.__buffer.handler_block(self.__sig1)
		self.__window.handler_block(self.__sig2)
		self.__view.handler_block(self.__sig3)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__buffer.handler_unblock(self.__sig1)
		self.__window.handler_unblock(self.__sig2)
		self.__view.handler_unblock(self.__sig3)
		self.__blocked = False
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

	def __matches_cb(self, manager, matches):
		self.__can_reset = True if matches else False
		if matches: self.__unblock()
		return False

	def __destroy(self):
		self.__reset()
		self.disconnect()
		del self
		return False

	def __changed_cb(self, *args):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(250, self.__reset_on_idle, priority=PRIORITY_LOW)
		return False

	def __key_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__reset, priority=PRIORITY_LOW)
		return True

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
