from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

SHOW_TOOLTIP_MESSAGE = _("Show hidden files and folders")
HIDE_TOOLTIP_MESSAGE = _("Hide hidden files and folders")

class Button(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__button.set_icon_name("view-restore")
		self.__toolbar.insert(self.__button, -1)
		self.__button.set_tooltip_text(SHOW_TOOLTIP_MESSAGE)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "toggle-hidden", self.__toggle_hidden_cb)
		self.connect(self.__button, "toggled", self.__toggled_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__toolbar = manager.gui.get_object("Toolbar")
		from gtk import ToggleToolButton
		self.__button = ToggleToolButton()
		return

	def __activate(self):
		signal = "show-hidden" if self.__button.get_active() else "hide-hidden"
		message = HIDE_TOOLTIP_MESSAGE if signal == "show-hidden" else SHOW_TOOLTIP_MESSAGE
		self.__button.set_tooltip_text(message)
		from gobject import idle_add
		idle_add(self.__manager.emit, signal)
		return False

	def __toggle(self):
		active = self.__button.get_active()
		self.__button.set_active(not active)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __toggled_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False

	def __toggle_hidden_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__toggle)
		return False
