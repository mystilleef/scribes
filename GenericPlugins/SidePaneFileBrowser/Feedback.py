from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

BUSY_MESSAGE = _("please wait...")

class Feedback(SignalManager):

	def __init__(self, manager, widget):
		SignalManager.__init__(self)
		self.__init_attributes(manager, widget)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "generate-uris", self.__folder_cb)
		self.connect(manager, "generate-uris-for-treenode", self.__busy_cb)
		# self.connect(manager, "generating-data-for-treeview", self.__busy_cb)
		self.connect(manager, "updated-model", self.__update_cb)

	def __init_attributes(self, manager, widget):
		self.__manager = manager
		self.__widget = widget
		self.__folder_uri = ""
		self.__label = manager.gui.get_object("StatusLabel")
		return

	def __show(self, message, bold=False, italic=False, color=None):
		if bold: message = "<b>%s</b>" % (message)
		if italic: message = "<i>%s</i>" % (message)
		if color: message = "<span color='%s'>%s</span>" % (color, message)
		self.__label.set_markup(message)
		self.__label.show()
		return False

	def __hide(self):
		self.__label.hide()
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

	def __update(self):
		self.__remove_timer(1)
		if self.__folder_uri:
			from gio import File
			self.__show("in ../%s/" % File(self.__folder_uri).get_basename(), True, False, "blue")
			from gobject import timeout_add
			self.__timer1 = timeout_add(10000, self.__hide)
		else:
			self.__hide()
		return False

	def __set_busy_message(self):
		self.__show(BUSY_MESSAGE, False, True, "red")
		return False

	def __busy_cb(self, *args):
		self.__folder_uri = ""
		self.__set_busy_message()
		return False

	def __folder_cb(self, manager, folder_uri):
		self.__folder_uri = folder_uri
		self.__set_busy_message()
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		# self.__update()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
