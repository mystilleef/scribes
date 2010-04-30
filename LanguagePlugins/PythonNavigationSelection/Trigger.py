from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger1, "activate", self.__activate_cb)
		self.connect(self.__trigger2, "activate", self.__activate_cb)
		self.connect(self.__trigger3, "activate", self.__activate_cb)
		self.connect(self.__trigger4, "activate", self.__activate_cb)
		self.connect(self.__trigger5, "activate", self.__activate_cb)
		self.connect(self.__trigger6, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"move-to-previous-block",
			"<alt>bracketleft",
			_("Move cursor to previous block"),
			_("Python")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"move-to-next-block",
			"<alt>bracketright",
			_("Move cursor to next block"),
			_("Python")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"select-python-block",
			"<alt>h",
			_("Select a block of code"),
			_("Python")
		)
		self.__trigger5 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"move-to-block-end",
			"<alt>e",
			_("Move cursor to end of block"),
			_("Python")
		)
		self.__trigger6 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"select-python-function",
			"<alt>f",
			_("Select function or method"),
			_("Python")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"select-python-class",
			"<alt>a",
			_("Select class"),
			_("Python")
		)
		self.__trigger4 = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return

	def __create_manager(self):
		from Manager import Manager
		manager = Manager(self.__editor)
		return manager

	def __activate_cb(self, trigger):
		if not self.__manager: self.__manager = self.__create_manager(self.__editor)
		function = {
			self.__trigger1: self.__manager.previous_block,
			self.__trigger2: self.__manager.next_block,
			self.__trigger3: self.__manager.select_function,
			self.__trigger4: self.__manager.select_class,
			self.__trigger5: self.__manager.select_block,
			self.__trigger6: self.__manager.end_of_block,
		}
		function[trigger]()
		return False
