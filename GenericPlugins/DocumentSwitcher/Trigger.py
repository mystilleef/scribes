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

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		name, shortcut, description, category = (
			"focus-next-window",
			"<ctrl>Page_Up",
			_("Focus next window"),
			_("Window Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		self.__trigger1.command = "next-window"
		name, shortcut, description, category = (
			"focus-previous-window",
			"<ctrl>Page_Down",
			_("Focus previous window"),
			_("Window Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__trigger2.command = "previous-window"
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __init_manager(self):
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def __activate(self, command):
		if not self.__manager: self.__init_manager()
		self.__manager.activate(command)
		return False

	def __activate_cb(self, trigger):
		from gobject import idle_add
		idle_add(self.__activate, trigger.command)
		return
