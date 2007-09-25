# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that defines the behavior of the
export dialog for the template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class ExportDialog(object):
	"""
	This class defines the behavior of the export dialog.
	"""

	def __init__(self, manager, editor, language):
		"""
		Initialize object.

		@param self: Reference to the ExportDialog instance.
		@type self: A ExportDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor, language)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__dialog.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_3 = self.__dialog.connect("response", self.__response_cb)
		self.__signal_id_4 = self.__dialog.connect("file-activated", self.__file_activated_cb)
		self.__signal_id_5 = self.__button.connect("clicked", self.__clicked_cb)
		self.__signal_id_6 = manager.connect("language-selected", self.__language_selected_cb)

	def __init_attributes(self, manager, editor, language):
		"""
		Initialize data attributes.

		@param self: Reference to the ExportDialog instance.
		@type self: A ExportDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "Template.glade")
		from gtk.glade import XML
		glade = XML(glade_file, "ExportDialog", domain="scribes")
		self.__dialog = glade.get_widget("ExportDialog")
		self.__button = glade.get_widget("ExportDialogExportButton")
		self.__language = language
		self.__manager = manager
		self.__editor = editor
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.
		"""
		self.__dialog.set_property("icon-name", "stock_save")
		self.__dialog.set_transient_for(self.__manager.glade.get_widget("TemplateEditorWindow"))
		from SCRIBES.dialogfilter import create_filter
		from i18n import msg0005
		xml_filter = create_filter(msg0005, "text/xml")
		self.__dialog.add_filter(xml_filter)
		from SCRIBES.info import home_folder, desktop_folder
		from os import path
		if path.exists(desktop_folder):
			self.__dialog.set_current_folder(desktop_folder)
		else:
			self.__dialog.set_current_folder(home_folder)
		return

	def show(self):
		"""
		Show the import dialog.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.
		"""
		self.__set_entry_text()
		self.__dialog.run()
		return

	def __set_entry_text(self):
		"""
		Set the default text in the entry field.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.
		"""
		name = self.__language + "-" + "templates.xml"
		self.__dialog.set_current_name(name)
		return

	def __hide(self):
		"""
		Hide the dialog.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.
		"""
		self.__editor.response()
		self.__dialog.hide()
		self.__editor.response()
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__signal_id_1, manager)
		disconnect_signal(self.__signal_id_2, self.__dialog)
		disconnect_signal(self.__signal_id_3, self.__dialog)
		disconnect_signal(self.__signal_id_4, self.__dialog)
		disconnect_signal(self.__signal_id_5, self.__button)
		disconnect_signal(self.__signal_id_6, manager)
		self.__button.destroy()
		self.__dialog.destroy()
		delete_attributes(self)
		self = None
		del self
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the "delete-event" signal is emitted.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.
		"""
		self.__hide()
		return True

	def __response_cb(self, *args):
		"""
		Handles callback when the "response" signal is emitted.

		@param self: Reference to the ExportDialog instance.
		@type self: An ExportDialog object.

		@param dialog: Reference to the ExportDialog instance.
		@type dialog: An ExportDialog object.

		@param response_id: A response identification.
		@type response_id: A Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__hide()
		return True

	def __file_activated_cb(self, *args):
		"""
		Handles callback when the "file-activated" signal is emitted.

		@param self: Reference to the ExportDialog instance.
		@type self: A ExportDialog object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__button.activate()
		return True

	def __clicked_cb(self, *args):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the ExportDialog instance.
		@type self: A ExportDialog object.
		"""
		name = self.__dialog.get_filename()
		from operator import not_
		if not_(name.endswith(".xml")): name = name + ".xml"
		self.__manager.emit("export-template", name)
		return True

	def __language_selected_cb(self, manager, language):
		"""
		Handles callback when the "language-selected" signal is emitted.

		@param self: Reference to the ExportDialog instance.
		@type self: A ExportDialog object.

		@param manager: Reference to the TemplateManager instance
		@type manager: A TemplateManager object.

		@param language: A language category.
		@type language: A String object.
		"""
		self.__language = language
		return
