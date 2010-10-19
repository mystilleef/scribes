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
		from Manager import Manager
		self.__manager = Manager(editor)
		name, shortcut, description, category = (
			"show-white-spaces", 
			"<alt>period", 
			_("Show or hide white spaces"), 
			_("Miscellaneous Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		self.__manager.destroy()
		del self
		return False

	def __activate_cb(self, *args):
		from DrawWhitespaceMetadata import get_value, set_value
		value = False if get_value() else True
		set_value(value)
		if value:
			icon = "yes"
			message = "Showing whitespace"
		else:
			icon = "no"
			message = "Hiding whitespace"
		self.__editor.update_message(message, icon, 7)
		return
