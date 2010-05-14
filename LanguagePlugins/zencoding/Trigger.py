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
		self.connect(self.__trigger9, "activate", self.__activate_cb)
		self.connect(self.__trigger10, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		name, shortcut, description, category = (
			"zencoding-toggle-comment",
			"<alt>c",
			_("Add or remove comments in most web languages"),
			_("Markup Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		self.__trigger1.zen_action = "toggle_comment"
		name, shortcut, description, category = (
			"zencoding-expand-abbreviation",
			"<ctrl>comma",
			_("Expand markup abbreviations"),
			_("Markup Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__trigger2.zen_action = "expand_abbreviation"
		name, shortcut, description, category = (
			"zencoding-next-edit-point",
			"<super>Right",
			_("Move cursor to next edit point"),
			_("Markup Operations")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		self.__trigger3.zen_action = "next_edit_point"
		name, shortcut, description, category = (
			"zencoding-previous-edit-point",
			"<super>Left",
			_("Move cursor to previous edit point"),
			_("Markup Operations")
		)
		self.__trigger4 = self.create_trigger(name, shortcut, description, category)
		self.__trigger4.zen_action = "prev_edit_point"
		name, shortcut, description, category = (
			"zencoding-remove-tag",
			"<super>r",
			_("Remove a tag"),
			_("Markup Operations")
		)
		self.__trigger5 = self.create_trigger(name, shortcut, description, category)
		self.__trigger5.zen_action = "remove_tag"
		name, shortcut, description, category = (
			"zencoding-select-in-tag",
			"<super>i",
			_("Select inner tag's content"),
			_("Markup Operations")
		)
		self.__trigger6 = self.create_trigger(name, shortcut, description, category)
		self.__trigger6.zen_action = "match_pair_inward"
		name, shortcut, description, category = (
			"zencoding-select-out-tag",
			"<super>o",
			_("Select outer tag's content"),
			_("Markup Operations")
		)
		self.__trigger7 = self.create_trigger(name, shortcut, description, category)
		self.__trigger7.zen_action = "match_pair_outward"
		name, shortcut, description, category = (
			"zencoding-split",
			"<super>j",
			_("Toggle between single and double tag"),
			_("Markup Operations")
		)
		self.__trigger8 = self.create_trigger(name, shortcut, description, category)
		self.__trigger8.zen_action = "split_join_tag"
		name, shortcut, description, category = (
			"zencoding-merge",
			"<super>m",
			_("Merge lines"),
			_("Markup Operations")
		)
		self.__trigger9 = self.create_trigger(name, shortcut, description, category)
		self.__trigger9.zen_action = "merge_lines"
		name, shortcut, description, category = (
			"zencoding-wrap-with-abbreviation",
			"<ctrl>e",
			_("Wrap with abbreviation"),
			_("Markup Operations")
		)
		self.__trigger10 = self.create_trigger(name, shortcut, description, category)
		self.__trigger10.zen_action = "wrap_with_abbreviation"
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		return False

	def __create_manager(self):
		from Manager import Manager
		manager = Manager(self.__editor)
		return manager

	def __activate(self, action):
		if not self.__manager: self.__manager = self.__create_manager()
		self.__manager.activate(action)
		return False

	def __activate_cb(self, trigger):
		from gobject import idle_add
		idle_add(self.__activate, trigger.zen_action)
		return
