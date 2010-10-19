from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger1, "activate", self.__activate_cb)
		self.connect(self.__trigger2, "activate", self.__activate_cb)
		from MenuItem import MenuItem
		MenuItem(editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"show-trigger-area-window",
			"",
			_("Show trigger area configuration window"),
			_("Miscellaneous Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		self.__trigger1.command = "show-trigger-area-window"
		name, shortcut, description, category = (
			"show-full-view",
			"<ctrl><alt>m",
			_("Show editor's full view"),
			_("Miscellaneous Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__trigger2.command = "show-full-view"
		from Manager import Manager
		self.__manager = Manager(editor)
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		self.__manager.destroy()
		del self
		return False

	def __activate(self, command):
		activate = {
			"show-trigger-area-window": self.__manager.show,
			"show-full-view": self.__manager.fullview,
		}
		activate[command]()
		return False

	def __activate_cb(self, trigger):
		from gobject import idle_add
		idle_add(self.__activate, trigger.command)
		return
