from gettext import gettext as _

from SCRIBES.SignalConnectionManager import SignalManager

COMMENT_MESSAGE = _("Commented line %s")
UNCOMMENT_MESSAGE = _("Uncommented line %s")
SELECTION_COMMENT_MESSAGE = _("Commented selected lines")
SELECTION_UNCOMMENT_MESSAGE = _("Uncommented selected lines")

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "comment", self.__comment_cb)
		self.connect(manager, "uncomment", self.__uncomment_cb)
		self.connect(manager, "finished", self.__finished_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__message = ""
		self.__has_selection = False
		return

	def __set_comment_message(self):
		if self.__has_selection:
			self.__message = SELECTION_COMMENT_MESSAGE
		else:
			self.__message = COMMENT_MESSAGE % (self.__editor.cursor.get_line() + 1)
		return False

	def __set_uncomment_message(self):
		if self.__has_selection:
			self.__message = SELECTION_UNCOMMENT_MESSAGE
		else:
			self.__message = UNCOMMENT_MESSAGE % (self.__editor.cursor.get_line() + 1)
		return False

	def __update(self):
		self.__editor.update_message(self.__message, "yes")
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate_cb(self, *args):
		self.__has_selection = self.__editor.has_selection
		return False

	def __comment_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set_comment_message)
		return False

	def __uncomment_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set_uncomment_message)
		return False

	def __finished_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
