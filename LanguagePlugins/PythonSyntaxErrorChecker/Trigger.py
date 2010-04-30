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
		self.__manager = None
		name, shortcut, description, category = (
			"check-python-syntax-errors", 
			"F2", 
			_("Check for syntax errors"), 
			_("Python")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		return

	def __activate_cb(self, *args):
		try:
			self.__manager.check()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.check()
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return
