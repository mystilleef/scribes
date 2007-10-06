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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that creates the about dialog for the
text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gtk import AboutDialog

class ScribesAboutDialog(AboutDialog):
	"""
	This class implements the about dialog for the text editor.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the dialog.

		@param self: Reference to the ScribesAboutDialog instance.
		@type self: A ScribesAboutDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		AboutDialog.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = self.connect("delete", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog's data attributes.

		@param self: Reference to the ScribesAboutDialog instance.
		@type self: A ScribesAboutDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__status_id = None
		self.__signal_id_1 = None
		return

	def __set_properties(self):
		"""
		Define the default properties of the dialog.

		@param self: Reference to the ScribesAboutDialog instance.
		@type self: A ScribesAboutDialog object.
		"""
		from i18n import msg0001
		# Set dialog properties.
		from gtk import about_dialog_set_url_hook
		from gnome import url_show
		about_dialog_set_url_hook(lambda self, url:url_show(self.__editor.website))
		self.set_artists(self.__editor.artists)
		self.set_authors(self.__editor.author)
		self.set_role("Scribes About Dialog")
		self.set_documenters(self.__editor.documenters)
		self.set_transient_for(self.__editor.window)
		self.set_property("comments", msg0001)
		self.set_property("copyright", self.__editor.copyrights)
		self.set_property("license", self.__editor.license.strip())
		self.set_property("logo-icon-name", "scribes")
		self.set_property("name", "Scribes")
		self.set_property("translator-credits", self.__editor.translators)
		self.set_property("version", self.__editor.version)
		self.set_property("website", self.__editor.website)
		self.set_property("website-label", self.__editor.website)
		self.set_property("icon-name", "stock_about")
		return

	def show_dialog(self):
		"""
		Show the dialog.

		@param self: Reference to the ScribesAboutDialog instance.
		@type self: A ScribesAboutDialog object.
		"""
		self.__editor.emit("show-dialog", self)
		from i18n import msg0002
		self.__status_id = self.__editor.feedback.set_modal_message(msg0002, "about")
		response = self.run()
		if response: self.hide_dialog()
		return

	def hide_dialog(self):
		"""
		Hide the dialog.

		@param self: Reference to the ScribesAboutDialog instance.
		@type self: A ScribesAboutDialog object.
		"""
		self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__editor.emit("hide-dialog", self)
		self.hide()
		return

	def __destroy_cb(self, dialog):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ScribesAboutDialog instance.
		@type self: A ScribesAboutDialog object.

		@param dialog: Reference to the ScribesAboutDialog instance.
		@type dialog: A ScribesAboutDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.destroy()
		del self
		self = None
		return
