from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__toggle_comment_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = ("toggle-comment", "<alt>c", _("(Un)comment line or selected lines"), _("Line"))
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def __toggle_comment_cb(self, *args):
		try:
			self.__manager.toggle_comment()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.toggle_comment()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		self.disconnect()
		self.remove_triggers()
		del self
		return
