# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class that creates the text editor's replace bar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from SCRIBES.bar import ScribesBar
from gtk import SHRINK, FILL, EXPAND
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class ReplaceBar(ScribesBar):
	"""
	This class creates the text editor's replace bar object. The class defines
	the behavior and default properties of the replace bar object.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the replace bar object.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesBar.__init__(self, editor)
		self.__init_attributes()
		self.__set_properties()
		self.__arrange_widgets()
		self.__signal_id_1 = self.__manager.connect("replacing", self.__replacebar_replacing_cb)
		self.__signal_id_2 = self.__manager.connect("replaced", self.__replacebar_replaced_cb)
		self.__signal_id_3 = self.__manager.connect("replaced-all", self.__replacebar_replaced_cb)
		self.__signal_id_4 = self.__manager.connect("cancel", self.__replacebar_cancel_cb)
		self.__signal_id_5 = self.__manager.connect("searching", self.__replacebar_searching_cb)
		self.__signal_id_6 = self.__manager.connect("matches-found", self.__replacebar_matches_found_cb)
		self.__signal_id_7 = self.__manager.connect("no-matches-found",
								self.__replacebar_no_matches_found_cb)
		self.__signal_id_8 = self.__entry.connect("activate", self.__replacebar_activate_cb)
		self.__signal_id_9 = self.__entry.connect("changed", self.__replacebar_changed_cb)
		self.__signal_id_10 = self.__matchcase_check_button.connect("toggled", self.__replacebar_toggled_cb)
		self.__signal_id_11 = self.__matchword_check_button.connect("toggled", self.__replacebar_toggled_cb)
		self.__signal_id_12 = self.__incremental_check_button.connect("toggled", self.__replacebar_toggled_cb)
		self.__signal_id_13 = self.__editor.connect("show-bar", self.__replacebar_show_bar_cb)
		self.__signal_id_14 = self.__editor.connect("hide-bar", self.__replacebar_hide_bar_cb)
		self.__signal_id_15 = self.connect("delete", self.__destroy_cb)
		self.__block_search_replace_signals()

########################################################################
#
#						Accessors
#
########################################################################

	def __get_search_replace_manager(self):
		return self.__search_replace_manager

	def __get_entry(self):
		return self.__entry

	def __get_match_case_button(self):
		return self.__matchcase_check_button

	def __get_match_word_button(self):
		return self.__matchword_check_button

	def __get_search_button(self):
		return self.__search_button

	def __get_next_button(self):
		return self.__next_button

	def __get_previous_button(self):
		return self.__previous_button

	def __get_stop_button(self):
		return self.__stop_button

	def __get_replace_entry(self):
		return self.__replace_entry

	def __get_replace_button(self):
		return self.__replace_button

	def __get_replace_all_button(self):
		return self.__replace_all_button

	def __get_incremental_check_button(self):
		return self.__incremental_check_button

########################################################################
#
#					Public API properties
#
########################################################################

	# Public API properties.
	search_replace_manager = property(__get_search_replace_manager, doc="Search and replace object.")
	find_text_entry = property(__get_entry, doc="Entry for the findbar.")
	match_case_button = property(__get_match_case_button, doc="")
	match_word_button = property(__get_match_word_button, doc="")
	next_button = property(__get_next_button, doc="")
	previous_button = property(__get_previous_button, doc="")
	search_button = property(__get_search_button, doc="")
	find_stop_button = property(__get_stop_button, doc="")
	replace_entry = property(__get_replace_entry, doc="")
	replace_button = property(__get_replace_button, doc="")
	replace_all_button = property(__get_replace_all_button, doc="")
	incremental_button = property(__get_incremental_check_button, doc="")

	def __init_attributes(self):
		"""
		Initialize the replace bar object's attributes.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.
		"""
		# Findbar stuff.
		self.__editor = self.editor
		self.__editor.triggermanager.trigger("initialize_search_replace_manager")
		self.__search_replace_manager = self.__manager = self.editor.store.get_object("SearchReplaceManager")
		from CaseButton import FindCaseButton
		self.__matchcase_check_button = FindCaseButton(self)
		from WordButton import FindWordButton
		self.__matchword_check_button = FindWordButton(self)
		from Entry import FindEntry
		self.__entry = FindEntry(self)
		from PreviousButton import FindPreviousButton
		self.__previous_button = FindPreviousButton(self)
		from NextButton import FindNextButton
		self.__next_button = FindNextButton(self)
		from SearchButton import FindSearchButton
		self.__search_button = FindSearchButton(self)
		from StopButton import FindStopButton
		self.__stop_button = FindStopButton(self)
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		self.__signal_id_7 = None
		self.__status_id_1 = None
		self.__signal_id_8 = self.__signal_id_9 = self.__signal_id_10 = None
		self.__signal_id_11 = self.__signal_id_12 = self.__signal_id_13 = None
		self.__signal_id_14 = self.__signal_id_15 = None
		from i18n import msg0005
		from gtk import Label
		self.__label = Label(msg0005)
		self.__show_stop_button = True
		self.__bar_is_visible = False
		# Replacebar stuff.
		self.__show_replace_stop_button = True
		from gtk import Label
		from i18n import msg0008
		self.__replace_label = Label(msg0008)
		self.__replace_label.set_use_underline(True)
		from ReplaceButton import ReplaceButton
		self.__replace_button = ReplaceButton(self)
		from ReplaceAllButton import ReplaceAllButton
		self.__replace_all_button = ReplaceAllButton(self)
		from ReplaceEntry import ReplaceEntry
		self.__replace_entry = ReplaceEntry(self)
		from ReplaceStopButton import ReplaceStopButton
		self.__replace_stop_button = ReplaceStopButton(self)
		from IncrementalButton import ReplaceIncrementalButton
		self.__incremental_check_button = ReplaceIncrementalButton(self)
		return

	def __set_properties(self):
		"""
		Define the default properties for the bar.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.
		"""
		self.set_property("name", "scribes replacebar")
		self.resize(rows=2, columns=7)
		self.set_col_spacings(5)
		self.set_row_spacings(1)
		self.set_property("border-width", 1)
		self.__label.set_use_underline(True)
		return

	def __arrange_widgets(self):
		"""
		Arrange the widgets of the replace bar.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.
		"""
		from gtk import SHRINK, FILL, EXPAND, Alignment, VSeparator
		from gtk import VSeparator, SHRINK, FILL, EXPAND, Alignment
		self.__find_alignment = Alignment(xalign=1.0, yalign=0.5)
		self.__find_alignment.add(self.__label)
		self.__label.set_mnemonic_widget(self.__entry)
		self.attach(child=self.__find_alignment,
					left_attach=0,
					right_attach=1,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=7,
					ypadding=0)

		self.attach(child=self.__entry,
					left_attach=1,
					right_attach=2,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__previous_button,
					left_attach=2,
					right_attach=3,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__search_button,
					left_attach=3,
					right_attach=4,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=VSeparator(),
					left_attach=4,
					right_attach=5,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=SHRINK|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__matchcase_check_button,
					left_attach=5,
					right_attach=6,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__matchword_check_button,
					left_attach=6,
					right_attach=7,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		# Replacebar
		self.__replace_alignment = Alignment(xalign=1.0, yalign=0.5)
		self.__replace_alignment.add(self.__replace_label)
		self.__replace_label.set_mnemonic_widget(self.__replace_entry)
		self.attach(child=self.__replace_alignment,
					left_attach=0,
					right_attach=1,
					top_attach=1,
					bottom_attach=2,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=7,
					ypadding=0)

		self.attach(child=self.__replace_entry,
					left_attach=1,
					right_attach=2,
					top_attach=1,
					bottom_attach=2,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__replace_button,
					left_attach=2,
					right_attach=3,
					top_attach=1,
					bottom_attach=2,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__replace_all_button,
					left_attach=3,
					right_attach=4,
					top_attach=1,
					bottom_attach=2,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=VSeparator(),
					left_attach=4,
					right_attach=5,
					top_attach=1,
					bottom_attach=2,
					xoptions=SHRINK|FILL,
					yoptions=SHRINK|FILL,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__incremental_check_button,
					left_attach=5,
					right_attach=6,
					top_attach=1,
					bottom_attach=2,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)
		return

	def show_bar(self):
		"""
		Show the findbar.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.
		"""
		if self.__bar_is_visible:
			return
		ScribesBar.show_bar(self)
		return

	def hide_bar(self):
		"""
		Hide the findbar.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.
		"""
		if self.__bar_is_visible is False:
			return
		ScribesBar.hide_bar(self)
		return

	def __show_replace_stop_button_cb(self):
		if self.__show_replace_stop_button is False:
			return False
		self.__replace_stop_button.set_property("sensitive", True)
		self.__replace_stop_button.grab_focus()
		return False

	def __show_stop_button_cb(self):
		"""
		Show the stop button.

		The stop button is shown if a searching operation is more than 1 second
		long.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		if self.__show_stop_button is False: return False
		self.__stop_button.set_property("sensitive", True)
		self.__stop_button.grab_focus()
		return False

########################################################################
#
#							(Un)Block Callbacks
#
########################################################################

	def __block_search_replace_signals(self):
		"""
		Block signals for the search and replace manager.

		The search and replace manager is used multiple widgets and
		functions. Thus when the find bar is hidden, these signals need
		to be blocked. Otherwise, the find bar traps these signals and
		handles them which can lead to unwanted behavior.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.
		"""
		self.__search_replace_manager.handler_block(self.__signal_id_1)
		self.__search_replace_manager.handler_block(self.__signal_id_2)
		self.__search_replace_manager.handler_block(self.__signal_id_3)
		self.__search_replace_manager.handler_block(self.__signal_id_4)
		self.__search_replace_manager.handler_block(self.__signal_id_5)
		self.__search_replace_manager.handler_block(self.__signal_id_6)
		self.__search_replace_manager.handler_block(self.__signal_id_7)
		return

	def __unblock_search_replace_signals(self):
		"""
		Unblock signals for the search and replace manager.

		The search and replace manager is used multiple widgets and
		functions. Thus when the find bar is hidden, these signals need
		to be blocked. Otherwise, the find bar traps these signals and
		handles them. This can lead to unwanted behavior.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.
		"""
		self.__search_replace_manager.handler_unblock(self.__signal_id_1)
		self.__search_replace_manager.handler_unblock(self.__signal_id_2)
		self.__search_replace_manager.handler_unblock(self.__signal_id_3)
		self.__search_replace_manager.handler_unblock(self.__signal_id_4)
		self.__search_replace_manager.handler_unblock(self.__signal_id_5)
		self.__search_replace_manager.handler_unblock(self.__signal_id_6)
		self.__search_replace_manager.handler_unblock(self.__signal_id_7)
		return

########################################################################
#
#					Signal and Event Handlers
#
########################################################################

	def __replacebar_replacing_cb(self, replacemanager):
		"""
		Handles callback when the "replacing" signal is emitted.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.

		@param replacemanager: The text editor's replace object.
		@type replacemanager: A ScribesReplaceBar object.
		"""
		self.__show_replace_stop_button = True
		self.__entry.set_property("sensitive", False)
		self.__search_button.set_property("sensitive", False)
		self.__matchcase_check_button.set_property("sensitive", False)
		self.__matchword_check_button.set_property("sensitive", False)
		from gobject import timeout_add
		timeout_add(1000, self.__show_replace_stop_button_cb)
		self.__previous_button.set_property("sensitive", False)
		if self.__next_button in self.get_children():
			self.remove(self.__next_button)
			from gtk import SHRINK, FILL, EXPAND
			self.attach(child=self.__search_button,
					left_attach=3,
					right_attach=4,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)
			self.__search_button.show_all()
		if self.__replace_all_button in self.get_children():
			self.remove(self.__replace_all_button)
			from gtk import SHRINK, FILL, EXPAND
			self.attach(child=self.__replace_stop_button,
						left_attach=3,
						right_attach=4,
						top_attach=1,
						bottom_attach=2,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__replace_stop_button.set_property("sensitive", False)
			self.__replace_stop_button.show_all()
		return

	def __replacebar_replaced_cb(self, replacemanager):
		"""
		Handles callback when the "replaced" signal is emitted.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.

		@param replacemanager: The text editor's replace object.
		@type replacemanager: A ScribesReplaceBar object.
		"""
		self.__show_replace_stop_button = False
		self.__entry.set_property("sensitive", True)
		self.__search_button.set_property("sensitive", True)
		self.__matchcase_check_button.set_property("sensitive", True)
		self.__matchword_check_button.set_property("sensitive", True)
		if self.__replace_stop_button in self.get_children():
			self.remove(self.__replace_stop_button)
			from gtk import SHRINK, FILL, EXPAND
			self.attach(child=self.__replace_all_button,
						left_attach=3,
						right_attach=4,
						top_attach=1,
						bottom_attach=2,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__replace_all_button.show_all()
		self.__entry.grab_focus()
		return

	def __replacebar_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the ScribesReplaceBar instance.
		@type self: A ScribesReplaceBar object.

		@param searchmanager: An object that performs search and replace operations.
		@type searchmanager: A SearchReplaceManager object.
		"""
		self.__show_replace_stop_button = False
		self.__entry.set_property("sensitive", True)
		self.__search_button.set_property("sensitive", True)
		self.__matchword_check_button.set_property("sensitive", True)
		self.__matchcase_check_button.set_property("sensitive", True)
		if self.__stop_button in self.get_children():
			self.remove(self.__stop_button)
		if self.__replace_stop_button in self.get_children():
			self.remove(self.__replace_stop_button)
			from gtk import SHRINK, FILL, EXPAND
			self.attach(child=self.__replace_all_button,
						left_attach=3,
						right_attach=4,
						top_attach=1,
						bottom_attach=2,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__replace_all_button.show_all()
		if not self.__search_button in self.get_children():
			from gtk import EXPAND, SHRINK, FILL
			self.attach(child=self.__search_button,
						left_attach=3,
						right_attach=4,
						top_attach=0,
						bottom_attach=1,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__search_button.show_all()
		self.__entry.grab_focus()
		return

	def __replacebar_searching_cb(self, searchmanager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param searchmanager: The text editor's searchmanager
		@type searchmanager: A SearchProcessor object.
		"""
		self.__search_replace_manager.reset()
		self.__show_stop_button = True
		from gobject import timeout_add
		timeout_add(1000, self.__show_stop_button_cb)
		if self.__search_button in self.get_children():
			self.remove(self.__search_button)
		if not self.__stop_button in self.get_children():
			from gtk import EXPAND, SHRINK, FILL
			self.attach(child=self.__stop_button,
					left_attach=3,
					right_attach=4,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)
		self.__stop_button.set_property("sensitive", False)
		self.__stop_button.show_all()
		return

	def __replacebar_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param searchmanager: The text editor's searchmanager
		@type searchmanager: A SearchProcessor object.
		"""
		self.__show_stop_button = False
		if self.__stop_button in self.get_children():
			self.remove(self.__stop_button)
		from gtk import EXPAND, SHRINK, FILL
		if self.__search_replace_manager.number_of_matches > 1:
			self.attach(child=self.__next_button,
						left_attach=3,
						right_attach=4,
						top_attach=0,
						bottom_attach=1,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__next_button.show_all()
		else:
			self.attach(child=self.__search_button,
						left_attach=3,
						right_attach=4,
						top_attach=0,
						bottom_attach=1,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__search_button.set_property("sensitive", False)
			self.__search_button.show_all()
		return

	def __replacebar_no_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param searchmanager: The text editor's searchmanager
		@type searchmanager: A SearchProcessor object.
		"""
		self.__show_stop_button = False
		if self.__stop_button in self.get_children():
			self.remove(self.__stop_button)
		if not self.__search_button in self.get_children():
			from gtk import EXPAND, SHRINK, FILL
			self.attach(child=self.__search_button,
						left_attach=3,
						right_attach=4,
						top_attach=0,
						bottom_attach=1,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__search_button.set_property("sensitive", False)
			self.__search_button.show_all()
		return

	def __replacebar_activate_cb(self, entry):
		"""
		Handles callback when the findbar's entry "activate" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param entry: The findbar's text entry.
		@type entry: A gtk.Entry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if self.__search_button in self.get_children():
			if entry.get_text(): self.__search_button.activate()
		else:
			if entry.get_text(): self.__next_button.activate()
		return True

	def __replacebar_changed_cb(self, entry):
		"""
		Handles callback when the findbar's entry "changed" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param entry: The findbar's text entry.
		@type entry: A gtk.Entry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import EXPAND, SHRINK, FILL
		self.__search_replace_manager.reset()
		if self.__next_button in self.get_children():
			self.remove(self.__next_button)
		if not self.__search_button in self.get_children():
			self.attach(child=self.__search_button,
						left_attach=3,
						right_attach=4,
						top_attach=0,
						bottom_attach=1,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__search_button.show_all()
		return False

	def __replacebar_toggled_cb(self, togglebutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param togglebutton: The findbar's case check button.
		@type togglebutton: A ScribesFindCaseButton object.
		"""
		if self.__next_button in self.get_children():
			self.remove(self.__next_button)
		if not self.__search_button in self.get_children():
			from gtk import EXPAND, SHRINK, FILL
			self.attach(child=self.__search_button,
					left_attach=3,
					right_attach=4,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)
			self.__search_button.show_all()
		self.__previous_button.set_property("sensitive", False)
		if self.__entry.get_text():
			self.__search_button.set_property("sensitive", True)
		else:
			self.__search_button.set_property("sensitive", False)
		self.__entry.grab_focus()
		self.__replace_button.set_property("sensitive", False)
		self.__replace_all_button.set_property("sensitive", False)
		self.__replace_entry.set_property("sensitive", False)
		return True

	def __replacebar_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param gotobar: The text editor's gotobar.
		@type gotobar: A ScribesFindBar object.
		"""
		if bar.get_property("name") != "scribes replacebar": return
		self.__bar_is_visible = True
		self.__unblock_search_replace_signals()
		from i18n import msg0009
		self.__status_id_1 = self.editor.feedback.set_modal_message(msg0009, "replace")
		self.set_property("sensitive", True)
		return

	def __replacebar_hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the ScribesFindBar instance.
		@type self: A ScribesFindBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param gotobar: The text editor's gotobar.
		@type gotobar: A ScribesFindBar object.
		"""
		if bar.get_property("name") != "scribes replacebar": return
		self.__block_search_replace_signals()
		self.__bar_is_visible = False
		self.__editor.feedback.unset_modal_message(self.__status_id_1, False)
		# Remove the next button from the findbar if it is attached.
		if self.__next_button in self.get_children():
			self.remove(self.__next_button)
		# Remove the stop button from the findbar if it is attached.
		if self.__stop_button in self.get_children():
			self.remove(self.__stop_button)
		# Attach the search button to the findbar if it isn't attached.
		if not self.__search_button in self.get_children():
			from gtk import SHRINK, FILL, EXPAND
			self.attach(child=self.__search_button,
					left_attach=3,
					right_attach=4,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND|FILL,
					xpadding=0,
					ypadding=0)
			self.__search_button.show_all()
		from i18n import msg0010
		self.editor.feedback.update_status_message(msg0010, "info", 3)
		if self.__replace_stop_button in self.get_children():
			self.remove(self.__replace_stop_button)
			from gtk import SHRINK, FILL, EXPAND
			self.attach(child=self.__replace_all_button,
						left_attach=3,
						right_attach=4,
						top_attach=1,
						bottom_attach=2,
						xoptions=SHRINK|FILL,
						yoptions=EXPAND|FILL,
						xpadding=0,
						ypadding=0)
			self.__replace_all_button.show_all()
		return

	def __destroy_cb(self, replacebar):
		"""
		Handles callback when "delete" signal is emitted.

		@param self: Reference to the ReplaceBar instance.
		@type self: A ReplaceBar object.

		@param replacebar: Reference to the ReplaceBar instance.
		@type replacebar: A ReplaceBar object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__matchword_check_button)
		self.__editor.disconnect_signal(self.__signal_id_11, self.__matchword_check_button)
		self.__editor.disconnect_signal(self.__signal_id_12, self.__incremental_check_button)
		self.__editor.disconnect_signal(self.__signal_id_13, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_14, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_15, self)
		self.destroy()
		del self
		self = None
		return
