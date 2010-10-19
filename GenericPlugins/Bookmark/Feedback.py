from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _
MESSAGE = _("Bookmarked lines")

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "add", self.__add_cb, True)
		self.connect(manager, "remove", self.__remove_cb, True)
		self.connect(manager, "remove-all", self.__remove_all_cb)
		self.connect(manager, "feedback", self.__feedback_cb)
		self.connect(manager, "show", self.__show_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "scroll-to-line", self.__scroll_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__feedback = True
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __mark(self, line):
		if not self.__feedback: return False
		message = _("Marked line %s") % str(line+1)
		self.__editor.update_message(message, "yes")
		return False

	def __unmark(self, line):
		if not self.__feedback: return False
		message = _("Unmarked line %s") % str(line+1)
		self.__editor.update_message(message, "yes")
		return False

	def __remove(self):
		if not self.__feedback: return False
		message = _("Removed all bookmarks")
		self.__editor.update_message(message, "yes")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, manager, line):
		from gobject import idle_add
		idle_add(self.__mark, line)
		return False

	def __remove_cb(self, manager, line):
		from gobject import idle_add
		idle_add(self.__unmark, line)
		return False

	def __remove_all_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__remove)
		return False

	def __feedback_cb(self, manager, feedback):
		self.__feedback = feedback
		return False

	def __show_cb(self, *args):
		self.__editor.set_message(MESSAGE)
		return False

	def __hide_cb(self, *args):
		self.__editor.unset_message(MESSAGE)
		return False

	def __scroll_cb(self, manager, line):
		message = _("Cursor on line %s") % str(line+1)
		self.__editor.update_message(message, "yes")
		return False
