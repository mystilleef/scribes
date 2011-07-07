from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

ICON = {
	"back": "stock_left",
	"up": "stock_up",
	"home": "stock_home",
}

SIGNAL = {
	"back": "go-back",
	"up": "go-up",
	"home": "go-home",
}

TOOLTIP = {
	"back": _("Show contents of previously visited folder"),
	"up": _("Show contents of parent folder"),
	"home": _("Show contents of home folder"),
}

class Button(SignalManager):

	def __init__(self, manager, editor, name):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor, name)
		self.__button.set_icon_name(ICON[name])
		self.__toolbar.insert(self.__button, -1)
		self.__button.set_tooltip_text(TOOLTIP[name])
		if name == "back": self.__button.set_property("sensitive", False)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "history-depth", self.__history_cb)
		self.connect(self.__button, "clicked", self.__clicked_cb)

	def __init_attributes(self, manager, editor, name):
		self.__manager = manager
		self.__editor = editor
		self.__toolbar = manager.gui.get_object("Toolbar")
		self.__name = name
		from gtk import ToolButton
		self.__button = ToolButton()
		return

	def __activate(self):
		from gobject import idle_add
		idle_add(self.__manager.emit, SIGNAL[self.__name])
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __clicked_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False

	def __history_cb(self, manager, history_depth):
		if self.__name != "back": return False
		sensitive = True if history_depth else False
		self.__button.set_property("sensitive", sensitive)
		return False
