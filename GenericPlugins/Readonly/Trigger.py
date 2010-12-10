from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"toggle-readonly",
			"F3",
			_("Toggle Readonly"),
			_("Miscellaneous Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		del self
		return False

	def __activate(self):
		self.__editor.toggle_readonly()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False
