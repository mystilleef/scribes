# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This modules documents a class that create the trigger that shows the
about window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates and manages the trigger that shows the about
	window.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__sig_id1 = self.__trigger.connect("activate", self.__show_about_dialog_cb)
		self.__sig_id2 = editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the AboutTrigger instance.
		@type self: A AboutTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__about_dialog = None
		self.__trigger = self.__create_trigger()
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

	def __create_trigger(self):
		"""
		Create a trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		# Trigger to show the about dialog.
		trigger = self.__editor.create_trigger("show_about_dialog")
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Trigger instance.
		@type self: An Trigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sig_id1, self.__trigger)
		self.__editor.disconnect_signal(self.__sig_id2, self.__editor.textview)
		if self.__about_dialog: self.__about_dialog.destroy_()
		del self
		self = None
		return

	def __show_about_dialog_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		try:
			self.__about_dialog.show_dialog()
		except AttributeError:
			from AboutDialog import Dialog
			self.__about_dialog = Dialog(self.__editor)
			self.__about_dialog.show_dialog()
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the AboutTrigger instance.
		@type self: An AboutTrigger object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from gtk import SeparatorMenuItem
		menu.append(SeparatorMenuItem())
		from PopupMenuItem import PopupMenuItem
		menu.append(PopupMenuItem(self.__editor))
		menu.show_all()
		return False
