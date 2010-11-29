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
		self.connect(self.__trigger7, "activate", self.__activate_cb)
		self.connect(self.__trigger8, "activate", self.__activate_cb)
		self.connect(editor.textview, "populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		name, shortcut, description, category = (
			"delete-line",
			"<alt>d",
			_("Delete line or selected lines"),
			_("Line Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"join-line",
			"<alt>j",
			_("Join current and next line(s)"),
			_("Line Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"free-line-above",
			"<alt><shift>o",
			_("Free current line"),
			_("Line Operations")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"free-line-below",
			"<alt>o",
			_("Free next line"),
			_("Line Operations")
		)
		self.__trigger4 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"delete-cursor-to-end",
			"<alt>End",
			_("Delete text from cursor to end of line"),
			_("Line Operations")
		)
		self.__trigger5 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"delete-cursor-to-start", 
			"<alt>Home", 
			_("Delete text from cursor to start of line"), 
			_("Line Operations")
		)
		self.__trigger6 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"duplicate-line", 
			"<ctrl>u", 
			_("Duplicate line or selected lines"), 
			_("Line Operations")
		)
		self.__trigger7 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"backward-word-deletion", 
			"<ctrl>BackSpace", 
			_("Duplicate line or selected lines"), 
			_("Line Operations")
		)
		self.__trigger8 = self.create_trigger(name, shortcut, description, category)
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
			"delete-line": self.__manager.delete_line,
			"join-line": self.__manager.join_line,
			"free-line-above": self.__manager.free_line_above,
			"free-line-below": self.__manager.free_line_below,
			"delete-cursor-to-start": self.__manager.delete_cursor_to_start,
			"delete-cursor-to-end": self.__manager.delete_cursor_to_end,
			"duplicate-line": self.__manager.duplicate_line,
			"backward-word-deletion": self.__manager.backward_word_deletion,
		}
		dictionary[trigger.name]()
		return False

	def __popup_cb(self, *args):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False
