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
import dialog for the template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class ImportDialog(object):
	"""
	This class defines the behavior of the import dialog.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the ImportDialog instance.
		@type self: A ImportDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__dialog.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_3 = self.__dialog.connect("response", self.__response_cb)
		self.__signal_id_4 = self.__dialog.connect("selection-changed", self.__selection_changed_cb)
		self.__signal_id_5 = self.__dialog.connect("file-activated", self.__file_activated_cb)
		self.__signal_id_6 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the ImportDialog instance.
		@type self: A ImportDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "Template.glade")
		from gtk.glade import XML
		glade = XML(glade_file, "ImportDialog", domain="scribes")
		self.__dialog = glade.get_widget("ImportDialog")
		self.__button = glade.get_widget("ImportDialogImportButton")
		self.__manager = manager
		self.__editor = editor
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.
		"""
		from i18n import msg0004
		self.__dialog.set_property("title", msg0004)
		width, height = self.__editor.calculate_resolution_independence(self.__editor.window,
														1.6, 1.929648241)
		self.__dialog.set_default_size(width, height)
		self.__dialog.set_property("icon-name", "stock_open")
		self.__dialog.set_transient_for(self.__manager.glade.get_widget("TemplateEditorWindow"))
		from SCRIBES.dialogfilter import create_filter
		from i18n import msg0005
		xml_filter = create_filter(msg0005, "text/xml")
		self.__dialog.add_filter(xml_filter)
		from os import path
		if path.exists(self.__editor.desktop_folder):
			self.__dialog.set_current_folder(self.__editor.desktop_folder)
		else:
			self.__dialog.set_current_folder(self.__editor.home_folder)
		return

	def show(self):
		"""
		Show the import dialog.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.
		"""
		self.__dialog.run()
		return

	def __hide(self):
		"""
		Hide the dialog.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.
		"""
		self.__editor.response()
		self.__dialog.hide()
		self.__editor.response()
		return

	def __import_template(self):
		"""
		Import templates from an XML file.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.
		"""
		try:
			from Exceptions import FileNotFoundError, InvalidFileError
			from Exceptions import ValidationError, NoDataError
			from operator import is_, not_
			self.__manager.emit("importing")
			xml_template_file = self.__dialog.get_filename()
			if is_(xml_template_file, None): raise FileNotFoundError
			from ImportTemplate import import_template_from_file
			templates = import_template_from_file(xml_template_file)
			if not_(templates): raise NoDataError
			language = templates[-1][-1]
			self.__manager.emit("imported-language", language)
		except FileNotFoundError:
			from i18n import msg0013
			self.__editor.error_dialog.show_message(msg0013, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		except InvalidFileError:
			from i18n import msg0014
			self.__editor.error_dialog.show_message(msg0014, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		except ValidationError:
			from i18n import msg0014
			self.__editor.error_dialog.show_message(msg0014, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		except NoDataError:
			from i18n import msg0015
			self.__editor.error_dialog.show_message(msg0015, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__button)
		self.__button.destroy()
		self.__dialog.destroy()
		self = None
		del self
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the "delete-event" signal is emitted.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.
		"""
		self.__hide()
		return True

	def __response_cb(self, *args):
		"""
		Handles callback when the "response" signal is emitted.

		@param self: Reference to the ImportDialog instance.
		@type self: An ImportDialog object.

		@param dialog: Reference to the ImportDialog instance.
		@type dialog: An ImportDialog object.

		@param response_id: A response identification.
		@type response_id: A Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__hide()
		return True

	def __selection_changed_cb(self, filechooser):
		"""
		Handles callback when the "selection-changed" signal is emitted.

		@param self: Reference to the ImportDialog instance.
		@type self: A ImportDialog object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		filename = filechooser.get_filename()
		if filename is None: return
		from os import path
		if path.isdir(filename):
			self.__button.set_property("sensitive", False)
		else:
			self.__button.set_property("sensitive", True)
		return True

	def __file_activated_cb(self, *args):
		"""
		Handles callback when the "file-activated" signal is emitted.

		@param self: Reference to the ImportDialog instance.
		@type self: A ImportDialog object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__button.activate()
		return True

	def __clicked_cb(self, *args):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the ImportDialog instance.
		@type self: A ImportDialog object.
		"""
		self.__import_template()
		return True
