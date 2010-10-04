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
		self.connect(self.__trigger3, "activate", self.__activate_cb)
		editor.get_toolbutton("OpenToolButton").props.sensitive = True
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"show-open-dialog", 
			"<ctrl>o", 
			_("Open a new file"), 
			_("File Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"show-remote-dialog", 
			"<ctrl>l", 
			_("Open a file at a remote location"), 
			_("File Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"show-newfile-dialog", 
			"<ctrl><shift>o", 
			_("Create a new file and open it"), 
			_("File Operations")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __create_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __activate_cb(self, trigger):
		if self.__manager is None: self.__manager = self.__create_manager()
		dictionary = {
			"show-open-dialog": self.__manager.show_open_dialog,
			"show-remote-dialog": self.__manager.show_remote_dialog,
			"show-newfile-dialog": self.__manager.show_newfile_dialog,
		}
		dictionary[trigger.name]()
		return False
