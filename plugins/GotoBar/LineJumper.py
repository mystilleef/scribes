from gettext import gettext as _

class Jumper(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("line-number", self.__line_number_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __jump_to(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line-1)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor(True)
		message = _("Moved view to line %d") % (line)
		self.__editor.update_message(message, "pass")
		return False

	def __destroy_cb(self,*args):
		self.__destroy()
		return False

	def __line_number_cb(self, manager, line):
		self.__jump_to(line)
		return False
