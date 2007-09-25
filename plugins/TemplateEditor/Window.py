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
This module documents a class that creates the template editor's window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TemplateWindow(object):
	"""
	This class creates the window for the template editor.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("show", self.__show_cb)
		self.__signal_id_3 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_4 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_5 = manager.connect("importing", self.__importing_cb)
		self.__signal_id_6 = manager.connect("import-error", self.__import_error_cb)
		self.__signal_id_7 = manager.connect("sensitive", self.__sensitive_cb)
		self.__signal_id_8 = self.__window.connect("drag-data-received", self.__drag_data_received_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__is_visible = False
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = None
		self.__window = manager.glade.get_widget("TemplateEditorWindow")
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.
		"""
		from SCRIBES.utils import calculate_resolution_independence
		width, height = calculate_resolution_independence(self.__editor.window, 1.6, 1.6)
		self.__window.set_property("default-width", width)
		self.__window.set_property("default-height", height)
		from gtk import WIN_POS_CENTER_ON_PARENT, DEST_DEFAULT_ALL
		self.__window.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		self.__window.set_property("destroy-with-parent", True)
		self.__window.set_transient_for(self.__editor.window)
		targets = [("text/uri-list", 0, 111)]
		from gtk.gdk import ACTION_COPY
		self.__window.drag_dest_set(DEST_DEFAULT_ALL, targets, ACTION_COPY)
		return

	def __show_window(self):
		"""
		Show window.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.
		"""
		self.__editor.response()
		self.__window.show_all()
		self.__is_visible = True
		self.__window.present()
		self.__editor.response()
		return

	def __hide_window(self):
		"""
		Hide window.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.
		"""
		self.__editor.response()
		self.__window.hide()
		self.__is_visible = False
		self.__manager.emit("hide")
		self.__editor.response()
		return

	def __import_template(self, xml_template_file):
		"""
		Import templates from an XML file.

		@param self: Reference to the TemplateWindow instance.
		@type self: An TemplateWindow object.
		"""
		try:
			from Exceptions import FileNotFoundError, InvalidFileError
			from Exceptions import ValidationError, DragDropError
			from operator import is_, not_
			self.__manager.emit("importing")
			if is_(xml_template_file, None): raise FileNotFoundError
			from ImportTemplate import import_template_from_file
			templates = import_template_from_file(xml_template_file)
			if not_(templates): raise NoDataError
			language = templates[-1][-1]
			self.__manager.emit("imported-language", language)
		except FileNotFoundError:
			from i18n import msg0013
			self.__editor.error_dialog.show_message(msg0013, parent_window=self.__window)
			self.__manager.emit("import-error")
			raise DragDropError
		except InvalidFileError:
			from i18n import msg0014
			self.__editor.error_dialog.show_message(msg0014, parent_window=self.__window)
			self.__manager.emit("import-error")
			raise DragDropError
		except ValidationError:
			from i18n import msg0014
			self.__editor.error_dialog.show_message(msg0014, parent_window=self.__window)
			self.__manager.emit("import-error")
			raise DragDropError
		except NoDataError:
			from i18n import msg0015
			self.__editor.error_dialog.show_message(msg0015, parent_window=self.__window)
			self.__manager.emit("import-error")
			raise DragDropError
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, manager)
		disconnect_signal(self.__signal_id_2, manager)
		disconnect_signal(self.__signal_id_3, self.__window)
		disconnect_signal(self.__signal_id_4, self.__window)
		disconnect_signal(self.__signal_id_5, manager)
		disconnect_signal(self.__signal_id_6, manager)
		disconnect_signal(self.__signal_id_7, manager)
		disconnect_signal(self.__signal_id_8, self.__window)
		self.__window.destroy()
		delete_attributes(self)
		self = None
		del self
		return

	def __show_cb(self, manager):
		"""
		Handles callback when the "show" signal is emitted.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.
		"""
		self.__show_window()
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the "delete-event" signal is emitted.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.
		"""
		self.__hide_window()
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the TemplateEditorWindow instance.
		@type self: A TemplateEditorWindow object.

		@param window: The template editor's window.
		@type window: A TemplateEditorWindow object.

		@param event: An event that occurs when the close button is pressed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from operator import not_, ne
		if not_(self.__is_visible): return False
		from gtk import keysyms
		if ne(event.keyval, keysyms.Escape): return False
		self.__hide_window()
		return True

	def __importing_cb(self, manager):
		"""
		Handles callback when the "importing" signal is emitted.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.response()
		self.__editor.feedback.start_busy_cursor()
		self.__window.set_property("sensitive", False)
		self.__editor.response()
		return

	def __import_error_cb(self, manager):
		"""
		Handles callback when the "import-error" signal is emitted.

		@param self: Reference to the TemplateWindow instance.
		@type self: A TemplateWindow object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.response()
		self.__editor.feedback.stop_busy_cursor()
		self.__window.set_property("sensitive", True)
		self.__editor.response()
		return

	def __sensitive_cb(self, manager, sensitive):
		self.__editor.response()
		self.__window.set_property("sensitive", sensitive)
		self.__editor.response()
		return

	def __drag_data_received_cb(self, window, context, x, y, selection_data, info, time):
		"""
		Handles callback when the "drag-data-received" signal is emitted.

		@param self: Reference to the TemplateEditorWindow instance.
		@type self: A TemplateEditorWindow object.

		@param window: Reference to the TemplateEditorWindow.
		@type window: A TemplateEditorWindow object.

		@param context: An object containing data about a drag selection.
		@type context: A gtk.DragContextData object.

		@param x: The x-cordinate of the drop.
		@type x: An Integer object.

		@param y: The y-cordinate of the drop.
		@type y: An Integer object.

		@param selection_data: Data representing the drag selection.
		@type selection_data: A gtk.SelectionData object.

		@param info: A unique identification for the text editor.
		@type info: An Integer object.

		@param time: The time the drop operation occurred.
		@type time: An Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from operator import ne, not_
		if ne(info, 111): return True
		self.__window.present()
		uris = selection_data.get_uris()
		from gnomevfs import get_local_path_from_uri
		from Exceptions import DragDropError
		for uri in uris:
			try:
				if not_(uri.startswith("file:///")): continue
				local_path = get_local_path_from_uri(uri)
				self.__import_template(local_path)
			except DragDropError:
				continue
		return True
