from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "found-matches", self.__matches_cb)
		self.connect(manager, "reset", self.__clear_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __clear(self):
		if not self.__marks: return
		del_ = self.__editor.delete_mark
		remove_marks = lambda start, end: (del_(start), del_(end))
		self.__editor.freeze()
		[remove_marks(*mark) for mark in self.__marks]
		self.__editor.thaw()
		self.__editor.refresh(False)
		self.__marks = []
		return False

	def __mark(self, matches):
		if not matches: return False
		self.__clear()
		mr = self.__editor.create_right_mark
		ml = self.__editor.create_left_mark
		iao = self.__editor.textbuffer.get_iter_at_offset
		iaos = lambda start, end: (iao(start), iao(end))
		mark_ = lambda start, end: (ml(start), mr(end))
		mark_from_offsets = lambda start, end: mark_(*(iaos(start, end)))
		marks = [mark_from_offsets(*offset) for offset in matches]
		self.__marks = marks
		self.__manager.emit("marked-matches", marks)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __clear_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__clear, priority=PRIORITY_LOW)
		return False

	def __matches_cb(self, manager, matches):
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__mark, matches, priority=PRIORITY_LOW)
		return False
