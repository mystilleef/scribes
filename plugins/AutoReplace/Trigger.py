from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__show_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		from MenuItem import MenuItem
		self.__menuitem = MenuItem(editor)
		self.__trigger = self.create_trigger("show-autoreplace-dialog")
		return

	def __show_cb(self, *args):
		self.__manager.show()
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		self.__menuitem.destroy()
		self.__manager.destroy()
		del self
		return
