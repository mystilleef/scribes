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
		self.connect(self.__trigger4, "activate", self.__activate_cb)
		self.connect(editor.textview, "populate-popup", self.__popup_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"select-word",
			"<alt>w",
			_("Select current word"),
			_("Selection Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"select-sentence",
			"<alt>s",
			_("Select current statement"),
			_("Selection Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"select-line",
			"<alt>l",
			_("Select current line"),
			_("Selection Operations")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"select-paragraph",
			"<alt>p",
			_("Select current paragraph"),
			_("Selection Operations")
		)
		self.__trigger4 = self.create_trigger(name, shortcut, description, category)
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
			self.__trigger1: self.__manager.select_word,
			self.__trigger2: self.__manager.select_statement,
			self.__trigger3: self.__manager.select_line,
			self.__trigger4: self.__manager.select_paragraph,
		}
		function[trigger]()
		return False

	def __popup_cb(self, *args):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False
