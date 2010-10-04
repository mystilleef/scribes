from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__show_window_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger = self.create_trigger("show-advanced-configuration-window")
		from MenuItem import MenuItem
		self.__menuitem = MenuItem(editor)
		return

	def __show_window_cb(self, *args):
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		if self.__menuitem: self.__menuitem.destroy()
		self.remove_triggers()
		self.disconnect()
		del self
		return

