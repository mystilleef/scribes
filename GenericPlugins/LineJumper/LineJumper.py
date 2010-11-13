from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Jumper(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "line-number", self.__line_number_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __jump_to(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line-1)
		self.__editor.move_view_to_cursor(True, iterator)
		self.__editor.textbuffer.place_cursor(iterator)
		message = _("Moved cursor to line %d") % (line)
		self.__editor.update_message(message, "pass")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __line_number_cb(self, manager, line):
		from gobject import idle_add
		idle_add(self.__jump_to, int(line))
		return False
