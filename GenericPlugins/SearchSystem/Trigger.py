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
		editor.get_toolbutton("SearchToolButton").props.sensitive = True
		editor.get_toolbutton("ReplaceToolButton").props.sensitive = True
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"show-findbar", 
			"<ctrl>f", 
			_("Search for text"), 
			_("Navigation Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"show-replacebar", 
			"<ctrl>r", 
			_("Search for and replace text"), 
			_("Navigation Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __get_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __activate_cb(self, trigger):
		if not self.__manager: self.__manager = self.__get_manager()
		function = {
			self.__trigger1: self.__manager.show,
			self.__trigger2: self.__manager.show_replacebar,
		}
		function[trigger]()
		return
