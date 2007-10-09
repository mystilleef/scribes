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
The modules exposes a class responsible for creating the findbar. The
findbar to search for text in the text editor's buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from SCRIBES.bar import ScribesBar
from gtk import SHRINK, FILL, EXPAND
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class FindBar(ScribesBar):
	"""
	This class creates a findbar object. The findbar allows users to move the
	cursor to a specific line in the document contained by the text editor.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the findbar object.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesBar.__init__(self, editor)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__arrange_widgets()
		self.__signal_id_1 = self.__search_replace_manager.connect("searching",
											self.__findbar_searching_cb)
		self.__signal_id_2 = self.__search_replace_manager.connect("matches-found",
											self.__findbar_matches_found_cb)
		self.__signal_id_3 = self.__search_replace_manager.connect("no-matches-found",
											self.__findbar_no_matches_found_cb)
		self.__signal_id_4 = self.__search_replace_manager.connect("cancel", self.__findbar_cancel_cb)
		self.__signal_id_5 = self.__entry.connect("activate", self.__findbar_activate_cb)
		self.__signal_id_6 = self.__entry.connect("changed", self.__findbar_changed_cb)
		self.__signal_id_7 = self.__matchcase_check_button.connect("toggled", self.findbar_toggled_cb)
		self.__signal_id_8 = self.__matchword_check_button.connect("toggled", self.findbar_toggled_cb)
		self.__signal_id_9 = self.__editor.connect("show-bar", self.__findbar_show_bar_cb)
		self.__signal_id_10 = self.__editor.connect("hide-bar", self.__findbar_hide_bar_cb)
		self.__signal_id_11 = self.connect("delete", self.__destroy_cb)
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

	def __init_attributes(self, editor):
		"""
		Initialize the object's data attributes.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		self.__editor = editor
		self.__editor.trigger("initialize_search_replace_manager")
		self.__search_replace_manager = self.__editor.get_object("SearchReplaceManager")
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
		self.__status_id_1 = None
		from i18n import msg0005
		from gtk import Label
		self.__label = Label(msg0005)
		self.__show_stop_button = True
		self.__bar_is_visible = False
		return

	def __set_properties(self):
		"""
		Define the find bar's properties.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		self.resize(rows=2, columns=7)
		self.set_col_spacings(5)
		self.set_row_spacings(1)
		self.set_property("border-width", 1)
		self.set_property("name", "scribes findbar")
		self.__label.set_use_underline(True)
		return

	def __arrange_widgets(self):
		"""
		Arrange the findbar's widgets.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		from gtk import VSeparator, SHRINK, FILL, EXPAND, Alignment
		self.__find_alignment = Alignment(xalign=0.0, yalign=0.5)
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
		return

	def show_bar(self):
		"""
		Show the findbar.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		if self.__bar_is_visible: return
		ScribesBar.show_bar(self)
		return

	def hide_bar(self):
		"""
		Hide the findbar.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		if self.__bar_is_visible is False: return
		ScribesBar.hide_bar(self)
		return

	def __findbar_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param gotobar: The text editor's gotobar.
		@type gotobar: A FindBar object.
		"""
		if bar.get_property("name") != "scribes findbar": return
		self.__bar_is_visible = True
		self.__unblock_search_replace_signals()
		from i18n import msg0006
		self.__status_id_1 = self.__editor.feedback.set_modal_message(msg0006, "find")
		return

	def __findbar_hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param gotobar: The text editor's gotobar.
		@type gotobar: A FindBar object.
		"""
		# Ignore all bars except the findbar.
		if bar.get_property("name") != "scribes findbar": return
		self.__bar_is_visible = False
		self.__block_search_replace_signals()
		self.__editor.feedback.unset_modal_message(self.__status_id_1, False)
		from i18n import msg0007
		self.__editor.feedback.update_status_message(msg0007, "info")
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
		return

	def __findbar_searching_cb(self, searchmanager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param searchmanager: The text editor's searchmanager
		@type searchmanager: A SearchProcessor object.
		"""
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

	def __show_stop_button_cb(self):
		"""
		Show the stop button.

		The stop button is shown if a searching operation is more than 1 second
		long.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		if self.__show_stop_button is False: return False
		self.__stop_button.set_property("sensitive", True)
		self.__stop_button.grab_focus()
		return False

	def __findbar_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

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

	def __findbar_no_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

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

	def __findbar_activate_cb(self, entry):
		"""
		Handles callback when the findbar's entry "activate" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param entry: The findbar's text entry.
		@type entry: A gtk.Entry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if self.__search_button in self.get_children():
			if entry.get_text():
				self.__search_button.activate()
		else:
			if entry.get_text():
				self.__next_button.activate()
		return True

	def __findbar_changed_cb(self, entry):
		"""
		Handles callback when the findbar's entry "changed" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

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

	def __findbar_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param searchmanager: The text editor's searchmanager
		@type searchmanager: A SearchProcessor object.
		"""
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
			self.__search_button.show_all()
		return

	def findbar_toggled_cb(self, togglebutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

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
		return True

	def __block_search_replace_signals(self):
		"""
		Block signals for the search and replace manager.

		The search and replace manager is used multiple widgets and
		functions. Thus when the find bar is hidden, these signals need
		to be blocked. Otherwise, the find bar traps these signals and
		handles them which can lead to unwanted behavior.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		self.__search_replace_manager.handler_block(self.__signal_id_1)
		self.__search_replace_manager.handler_block(self.__signal_id_2)
		self.__search_replace_manager.handler_block(self.__signal_id_3)
		self.__search_replace_manager.handler_block(self.__signal_id_4)
		return

	def __unblock_search_replace_signals(self):
		"""
		Unblock signals for the search and replace manager.

		The search and replace manager is used multiple widgets and
		functions. Thus when the find bar is hidden, these signals need
		to be blocked. Otherwise, the find bar traps these signals and
		handles them. This can lead to unwanted behavior.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.
		"""
		self.__search_replace_manager.handler_unblock(self.__signal_id_1)
		self.__search_replace_manager.handler_unblock(self.__signal_id_2)
		self.__search_replace_manager.handler_unblock(self.__signal_id_3)
		self.__search_replace_manager.handler_unblock(self.__signal_id_4)
		return

	def __destroy_cb(self, findbar):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the FindBar instance.
		@type self: A FindBar object.

		@param findbar: Reference to the FindBar instance.
		@type findbar: A FindBar object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__search_replace_manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__search_replace_manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__search_replace_manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__search_replace_manager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__matchcase_check_button)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__matchword_check_button)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_11, self)
		self.destroy()
		del self
		self = None
		return
