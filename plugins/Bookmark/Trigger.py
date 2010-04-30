from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(editor.textview, "populate-popup", self.__popup_cb)
		self.connect(self.__trigger1, "activate", self.__activate_cb)
		self.connect(self.__trigger2, "activate", self.__activate_cb)
		self.connect(self.__trigger3, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		from Manager import Manager
		self.__manager = Manager(editor)
		self.__editor = editor
		name, shortcut, description, category = (
			"toggle-bookmark", 
			"<ctrl>d", 
			_("Add or remove bookmark on a line"), 
			_("Navigation")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"remove-all-bookmarks", 
			"<ctrl><alt>b", 
			_("Remove all bookmarks"), 
			_("Navigation")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"show-bookmark-browser", 
			"<ctrl>b", 
			_("Navigate bookmarks"), 
			_("Naviagtion")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		self.__browser = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return

	def __popup_cb(self, textview, menu):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False

	def __activate_cb(self, trigger):
		function ={
			self.__trigger1: self.__manager.toggle,
			self.__trigger2: self.__manager.remove,
			self.__trigger3: self.__manager.show,
		}
		function[trigger]()
		return False
