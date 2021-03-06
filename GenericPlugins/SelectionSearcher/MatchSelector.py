from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "current-match", self.__match_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __select(self, mark):
		giam = self.__editor.textbuffer.get_iter_at_mark
		start = giam(mark[0])
		end = giam(mark[1])
		self.__editor.textbuffer.select_range(start, end)
		self.__editor.textview.scroll_mark_onscreen(mark[1])
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

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __match_cb(self, manager, mark):
		self.__remove_timer(1)
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__select, mark, priority=PRIORITY_LOW)
		return False
