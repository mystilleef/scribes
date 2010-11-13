from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Label(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "show", self.__show_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.gui.get_object("LineLabel")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __update(self):
		message = _("of <b>%d</b>") % self.__editor.textbuffer.get_line_count()
		self.__label.set_label(message)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__update()
		return False
