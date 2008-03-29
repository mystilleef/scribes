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
This module documents the class that creates the about window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gtk import AboutDialog

class Dialog(AboutDialog):
	"""
	This class implements the about window.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the AboutDialog instance.
		@type self: A AboutDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		AboutDialog.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()

	def __init_attributes(self, editor):
		"""
		Initialize attributes.

		@param self: Reference to the AboutDialog instance.
		@type self: A AboutDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__status_id = None
		return

	def __set_properties(self):
		"""
		Define the default properties of the dialog.

		@param self: Reference to the AboutDialog instance.
		@type self: A AboutDialog object.
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

		@param self: Reference to the AboutDialog instance.
		@type self: A AboutDialog object.
		"""
		self.__editor.emit("show-dialog", self)
		from i18n import msg0002
		self.__status_id = self.__editor.set_message(msg0002, "about")
		self.show_all()
		response = self.run()
		if response: self.hide_dialog()
		return

	def hide_dialog(self):
		"""
		Hide the dialog.

		@param self: Reference to the AboutDialog instance.
		@type self: A AboutDialog object.
		"""
		self.__editor.unset_message(self.__status_id)
		self.__editor.emit("hide-dialog", self)
		self.hide()
		return

	def __destroy(self):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AboutDialog instance.
		@type self: A AboutDialog object.
		"""
		self.destroy()
		del self
		self = None
		return

	def destroy_(self):
		self.__destroy()
		return
