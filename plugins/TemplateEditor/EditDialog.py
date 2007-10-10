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
This module documents a class that defines the behavior of the edit
dialog from the template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class EditDialog(object):
	"""
	This class defines the behavior of the edit dialog.
	"""

	def __init__(self, manager, editor, language, trigger):
		"""
		Initialize object.

		@param self: Reference to the EditDialog instance.
		@type self: A EditDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param language: The language of category of a template.
		@type language: A String object.

		@param trigger: A template trigger.
		@type trigger: A String object.
		"""
		self.__init_attributes(manager, editor, language, trigger)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("template-selected", self.__template_selected_cb)
		self.__signal_id_3 = self.__dialog.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_4 = self.__save_button.connect("clicked", self.__save_clicked_cb)
		self.__signal_id_5 = self.__cancel_button.connect("clicked", self.__cancel_clicked_cb)
		self.__signal_id_6 = self.__name_entry.connect("changed", self.__changed_cb)
		self.__signal_id_7 = self.__dialog.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, manager, editor, language, trigger):
		"""
		Initialize data attributes.

		@param self: Reference to the EditDialog instance.
		@type self: A EditDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param language: The language category of a template.
		@type language: A String object.

		@param trigger: A template trigger.
		@type trigger: A String object.
		"""
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "Template.glade")
		from gtk.glade import XML
		self.__glade = glade = XML(glade_file, "EditorDialog", domain="scribes")
		self.__dialog = glade.get_widget("EditorDialog")
		self.__manager = manager
		self.__editor = editor
		self.__language = language
		self.__trigger = trigger
		self.__name_label = glade.get_widget("EditorDialogNameLabel")
		self.__description_label = glade.get_widget("EditorDialogDescriptionLabel")
		self.__buffer_label = glade.get_widget("EditorDialogTemplateLabel")
		self.__name_entry = glade.get_widget("EditorDialogNameEntry")
		self.__description_entry = glade.get_widget("EditorDialogDescriptionEntry")
		from Editor import Editor
		self.__buffer = Editor(manager, editor, language)
		self.__save_button = glade.get_widget("EditorDialogSaveButton")
		self.__cancel_button = glade.get_widget("EditorDialogCancelButton")
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.
		"""
		scrollwin = self.__glade.get_widget("EditorDialogScrolledWindow")
		scrollwin.add(self.__buffer)
		width, height = self.__editor.calculate_resolution_independence(self.__editor.window, 2, 2.133333333)
		self.__dialog.set_property("default-width", width)
		self.__dialog.set_property("default-height", height)
		from i18n import msg0006
		self.__dialog.set_property("title", msg0006)
		self.__dialog.set_property("icon-name", "gnome-settings")
		self.__dialog.set_transient_for(self.__manager.glade.get_widget("TemplateEditorWindow"))
		self.__name_label.set_mnemonic_widget(self.__name_entry)
		self.__description_label.set_mnemonic_widget(self.__description_entry)
		self.__buffer_label.set_mnemonic_widget(self.__buffer)
		return

	def show(self):
		"""
		Show dialog.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.
		"""
		self.__manager.emit("sensitive", False)
		trigger, description, template = self.__get_template_info()
		self.__reset_widgets(trigger, description, template)
		self.__editor.response()
		self.__dialog.show_all()
		self.__editor.response()
		return

	def __hide(self, sensitive=True):
		"""
		Hide dialog.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.
		"""
		self.__editor.response()
		self.__manager.emit("sensitive", sensitive)
		self.__dialog.hide()
		self.__editor.response()
		return

	def __get_template_info(self):
		"""
		Get template information from database.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@return: Template information.
		@rtype: A Tuple object.
		"""
		from Metadata import open_template_database
		from Metadata import close_template_database
		database = open_template_database()
		key = self.__language + self.__trigger
		description = database[key][0]
		template = database[key][1]
		close_template_database(database)
		return self.__trigger, description, template

	def __reset_widgets(self, trigger, description, template):
		"""
		Set default text in widgets.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@param trigger: A template trigger.
		@type trigger: A String object.

		@param description: Description of a template.
		@type description: A String object.

		@param template: A template.
		@type template: A String object.
		"""
		self.__name_entry.set_text(trigger)
		self.__description_entry.set_text(description)
		self.__buffer.get_buffer().set_text(template)
		self.__name_entry.grab_focus()
		return

	def __check_name_entry(self):
		"""
		Validate template trigger.

		Whether or not the trigger entered in the name entry field
		is valid.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.
		"""
		from operator import not_, contains
		from Exceptions import EntryError, SameTriggerError
		if not_(self.__name_entry.get_text().strip()): raise EntryError
		database_key = self.__language + self.__name_entry.get_text().strip()
		from Metadata import open_template_database
		from Metadata import close_template_database
		database = open_template_database()
		keys = database.keys()
		keys.remove(self.__language+self.__trigger)
		close_template_database(database)
		if contains(keys, database_key): raise SameTriggerError
		return

	def __update_template_database(self):
		"""
		Update the template database.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.
		"""
		from Metadata import open_template_database
		from Metadata import close_template_database
		database = open_template_database("w")
		del database[self.__language+self.__trigger]
		trigger = self.__name_entry.get_text().strip()
		description = self.__description_entry.get_text().strip()
		txtbuffer = self.__buffer.get_buffer()
		start, end = txtbuffer.get_bounds()
		template = txtbuffer.get_text(start, end)
		database[self.__language+trigger] = (description, template)
		close_template_database(database)
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@param manager: Reference to the TemplateManager.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__save_button)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__cancel_button)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__name_entry)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__dialog)
		self.__save_button.destroy()
		self.__cancel_button.destroy()
		self.__dialog.destroy()
		self = None
		del self
		return

	def __template_selected_cb(self, manager, data):
		"""
		Handles callback when the "template-selected" signal is emitted.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param data: Selection information.
		@type data: A Tuple object.
		"""
		self.__language, self.__trigger = data
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.
		"""
		self.__hide()
		return True

	def __save_clicked_cb(self, *args):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		try:
			from Exceptions import EntryError, SameTriggerError
			self.__check_name_entry()
			self.__hide(False)
			self.__manager.emit("trigger-selected", self.__name_entry.get_text().strip())
			self.__update_template_database()
		except EntryError:
			from i18n import msg0007
			self.__editor.error_dialog.show_message(msg0007, parent_window=self.__dialog)
		except SameTriggerError:
			from i18n import msg0008
			self.__editor.error_dialog.show_message(msg0008, parent_window=self.__dialog)
		return True

	def __cancel_clicked_cb(self, *args):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__hide()
		return True

	def __changed_cb(self, entry):
		"""
		Handles callback when the "changed" signal is emitted.

		@param self: Reference to the EditDialog instance.
		@type self: An EditDialog object.

		@param entry: The name text entry field.
		@type entry: A gtk.Entry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__editor.response()
		if self.__name_entry.get_text().strip():
			self.__description_entry.set_property("sensitive", True)
			self.__buffer.set_property("sensitive", True)
			self.__save_button.set_property("sensitive", True)
		else:
			self.__description_entry.set_property("sensitive", False)
			self.__buffer.set_property("sensitive", False)
			self.__save_button.set_property("sensitive", False)
		self.__editor.response()
		return False

	def __key_press_event_cb(self, dialog, event):
		from gtk import keysyms
		from operator import ne
		if ne(event.keyval, keysyms.Escape): return False
		self.__hide()
		return True
