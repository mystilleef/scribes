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
			"close-reopen", 
			"<ctrl><shift>n", 
			_("Close current window and reopen a new one"), 
			_("Window Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		return

	def __activate_cb(self, *args):
		self.__editor.new()
		self.__editor.close()
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		del self
		self = None
		return
