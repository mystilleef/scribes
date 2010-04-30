from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)
		editor.get_toolbutton("PreferenceToolButton").props.sensitive = True

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"show-preferences-window", 
			"F12", 
			_("Show preferences window"), 
			_("General Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __activate(self):
		try :
			self.__manager.show()
		except AttributeError :
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show()
		finally:
			self.__editor.response()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return
