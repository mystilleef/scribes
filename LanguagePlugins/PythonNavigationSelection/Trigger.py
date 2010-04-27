from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__prv_trigger, "activate", self.__prv_block_cb)
		self.connect(self.__nxt_trigger, "activate", self.__nxt_block_cb)
		self.connect(self.__select_trigger, "activate", self.__select_block_cb)
		self.connect(self.__end_trigger, "activate", self.__end_block_cb)
		self.connect(self.__select_function_trigger, "activate", self.__select_function_cb)
		self.connect(self.__select_class_trigger, "activate", self.__select_class_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = ("move-to-previous-block", "<alt>bracketleft", _("Move cursor to previous block"), _("Python"))
		self.__prv_trigger = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = ("move-to-next-block", "<alt>bracketright", _("Move cursor to next block"), _("Python"))
		self.__nxt_trigger = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = ("select-python-block", "<alt>h", _("Select a block of code"), _("Python"))
		self.__select_trigger = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = ("move-to-block-end", "<alt>e", _("Move cursor to end of block"), _("Python"))
		self.__end_trigger = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = ("select-python-function", "<alt>f", _("Select function or method"), _("Python"))
		self.__select_function_trigger = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = ("select-python-class", "<alt>a", _("Select class"), _("Python"))
		self.__select_class_trigger = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def __get_manager(self):
		if self.__manager: return self.__manager
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return self.__manager

	def __prv_block_cb(self, *args):
		self.__get_manager().previous_block()
		return

	def __nxt_block_cb(self, *args):
		self.__get_manager().next_block()
		return

	def __select_function_cb(self, *args):
		self.__get_manager().select_function()
		return

	def __select_class_cb(self, *args):
		self.__get_manager().select_class()
		return

	def __select_block_cb(self, *args):
		self.__get_manager().select_block()
		return

	def __end_block_cb(self, *args):
		self.__get_manager().end_of_block()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		self.disconnect()
		self.remove_triggers()
		return

