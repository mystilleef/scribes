from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger1, "activate", self.__activate_cb)
		self.connect(self.__trigger2, "activate", self.__activate_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		name, shortcut, description, category = (
			"select-next-highlighted-match", 
			"<ctrl>g", 
			_("Navigate to next highlighted match"), 
			_("Navigation Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		self.__trigger1.action = "select-next-match"
		name, shortcut, description, category = (
			"select-previous-highlighted-match", 
			"<ctrl><shift>g", 
			_("Navigation to previous highlighted match"), 
			_("Navigation Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__trigger2.action = "select-previous-match"
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		self.__manager.destroy()
		del self
		return False

	def __activate(self, action):
		self.__manager.activate(action)
		return False

	def __activate_cb(self, trigger):
		from gobject import idle_add
		idle_add(self.__activate, trigger.action)
		return
