from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

RUN_MESSAGE = _("please wait...")
COMMENT_MESSAGE = _("Commented line %s")
COMMENTS_MESSAGE = _("Commented lines")
UNCOMMENT_MESSAGE = _("Uncommented line %s")
UNCOMMENTS_MESSAGE = _("Uncommented lines")

class Manager(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "commenting", self.__commenting_cb)
		self.connect(manager, "single-line-boundary", self.__single_boundary_cb)
		self.connect(manager, "multiline-boundary", self.__multi_boundary_cb)
		self.connect(manager, "processed-text", self.__text_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__boundaries = ()
		self.__commenting = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self):
		self.__editor.unset_message(RUN_MESSAGE, "run")
		if self.__commenting:
			if self.__boundaries:
				line_number = self.__buffer.get_iter_at_mark(self.__boundaries[0]).get_line() + 1
				message = COMMENT_MESSAGE % line_number
				self.__editor.update_message(message, "yes", 5)
			else:
				self.__editor.update_message(COMMENTS_MESSAGE, "yes", 5)
		else:
			if self.__boundaries:
				line_number = self.__buffer.get_iter_at_mark(self.__boundaries[0]).get_line() + 1
				message = UNCOMMENT_MESSAGE % line_number
				self.__editor.update_message(message, "yes", 5)
			else:
				self.__editor.update_message(UNCOMMENTS_MESSAGE, "yes", 5)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		self.__editor.set_message(RUN_MESSAGE, "run")
		return False

	def __multi_boundary_cb(self, manager, boundaries):
		self.__boundaries = ()
		return False

	def __single_boundary_cb(self, manager, boundaries):
		self.__boundaries = boundaries
		return False

	def __commenting_cb(self, manager, commenting):
		self.__commenting = commenting
		return False

	def __text_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False
