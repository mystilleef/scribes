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
This module exposes a base class for all dialogs used by the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Dialog

class ScribesDialog(Dialog):
	"""
	This class defines the basic properties and behavior for all dialogs of the
	text editor. Its primary objective is for inheritance. It inherits from the
	gtk.Dialog. See the GTK+ manual for the properties gtk.Dialog exposes.
	Ideally all dialogs should inherits from this class. Dialogs are shown or
	hidden but never destroyed.
	"""

	def __init__(self, editor):
		"""
		Initialize basic dialog attributes and properties.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.

		@param window: An optional parent window.
		@type window: A gtk.Window object.
		"""
		Dialog.__init__(self)
		self.__init_attributes(editor)
		self.__set_dialog_properties()
		self.__signal_id_1 = self.connect("close", self.__close_cb)
		self.__signal_id_2 = self.connect("response", self.__close_cb)
		self.__signal_id_3 = self.editor.connect("close-document", self.__destroy_cb)
		self.__signal_id_4 = self.editor.connect("close-document-no-save", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog attributes.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.

		@param window: A optional parent window.
		@type window: A gtk.Window object.
		"""
		self.editor = editor
		return

	def __set_dialog_properties(self):
		"""
		Set the default dialog properties.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
		"""
		self.set_property("has-separator", False)
		self.set_property("skip-pager-hint", True)
		self.set_property("skip-taskbar-hint", True)
		self.set_property("urgency-hint", False)
		self.set_property("modal", True)
		from gtk import WIN_POS_CENTER_ON_PARENT
		self.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		self.set_property("resizable", True)
		try:
			self.set_transient_for(self.editor.window)
		except:
			pass
		return

	def show_dialog(self):
		"""
		Show the dialog.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
		"""
		self.editor.emit("show-dialog", self)
		self.run()
		return

	def hide_dialog(self):
		"""
		Hide the dialog.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
		"""
		self.editor.emit("hide-dialog", self)
		self.hide()
		# Feedback to the text editor's statusbar indication the dialog window
		# has just been closed.
		try:
			from internationalization import msg0187
			self.editor.feedback.update_status_message(msg0187, "info", 1)
		except:
			pass
		return

	def __destroy(self):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the OpenDialog instance.
		@type self: An OpenDialog object.

		@param dialog: Reference to the OpenDialog instance.
		@type dialog: An OpenDialog object.
		"""
		self.editor.disconnect_signal(self.__signal_id_1, self)
		self.editor.disconnect_signal(self.__signal_id_2, self)
		self.editor.disconnect_signal(self.__signal_id_3, self.editor)
		self.editor.disconnect_signal(self.__signal_id_4, self.editor)
		self.destroy()
		del self
		self = None
		return

################################################################################
#
#							Dialog  Callbacks
#
################################################################################

	def __close_cb(self, *args):
		self.hide_dialog()
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
