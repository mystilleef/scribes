from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		editor.refresh()
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)
		editor.refresh()

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"open-recent-files", 
			"<ctrl><alt>r", 
			_("Open recent files"), 
			_("File Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		from Manager import Manager
		self.__manager = Manager(editor)
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __activate(self):
		self.__editor.refresh()
		self.__manager.activate()
		self.__editor.refresh()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False
