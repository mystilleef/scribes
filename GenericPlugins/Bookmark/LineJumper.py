from SCRIBES.SignalConnectionManager import SignalManager

class Jumper(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "scroll-to-line", self.__scroll_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __scroll_to(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.textview.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __scroll_cb(self, manager, line):
		from gobject import idle_add
		idle_add(self.__scroll_to, line)
		return False
