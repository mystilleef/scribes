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
This module documents a class that defines the behavior of a modification
dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class ModificationDialog(object):
	"""
	This class defines the behavior of a modification dialog. The dialog
	provides options to reload, overwrite or ignore changes made to
	a document opened by Scribes by another application.
	"""

	def __init__(self, filesaver, editor):
		"""
		Initialize object.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.

		@param filesaver: An object that saves documents.
		@type filesaver: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(filesaver, editor)
		self.__set_properties()
		self.__signal_id_1 = self.__ignore_button.connect("clicked", self.__ignore_clicked_cb)
		self.__signal_id_2 = self.__overwrite_button.connect("clicked", self.__overwrite_clicked_cb)
		self.__signal_id_3 = self.__reload_button.connect("clicked", self.__reload_clicked_cb)
		self.__signal_id_4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_5 = self.__window.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, filesaver, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.

		@param filesaver: An object that saves documents.
		@type filesaver: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__filesaver = filesaver
		from os.path import join
		glade_file = join(self.__editor.scribes_data_folder, "ModificationDialog.glade")
		from gtk.glade import XML
		glade = XML(glade_file, "Window")
		self.__window = glade.get_widget("Window")
		self.__ignore_button = glade.get_widget("IgnoreButton")
		self.__overwrite_button = glade.get_widget("OverwriteButton")
		self.__reload_button = glade.get_widget("ReloadButton")
		self.__label = glade.get_widget("MessageLabel")
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__window.set_transient_for(self.__editor.window)
		self.__window.set_property("icon-name", "gtk-dialog-warning")
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__ignore_button)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__overwrite_button)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__reload_button)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__window)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__window)
		self.__ignore_button.destroy()
		self.__overwrite_button.destroy()
		self.__reload_button.destroy()
		self.__window.destroy()
		self = None
		del self
		return

	def show(self):
		"""
		Show dialog.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__editor.response()
		from internationalization import msg0490
		message = "<b>" + msg0490 + "</b>"
		from gnomevfs import get_local_path_from_uri
		message = message % (get_local_path_from_uri(self.__editor.uri))
		self.__label.set_markup(message)
		self.__ignore_button.grab_focus()
		self.__editor.emit("show-dialog", self.__window)
		self.__window.show_all()
		self.__editor.response()
		return

	def __hide(self):
		"""
		Hide dialog.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__editor.response()
		self.__editor.emit("hide-dialog", self.__window)
		self.__window.hide()
		self.__editor.response()
		return

	def __ignore_clicked_cb(self, *args):
		"""
		Handles callback when the ignore button is clicked.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__filesaver.reset_save_flag()
		self.__hide()
		return True

	def __overwrite_clicked_cb(self, *args):
		"""
		Handles callback when the overwrite button is clicked.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__filesaver.reset_save_flag()
		self.__editor.trigger("save_file")
		self.__hide()
		return True

	def __reload_clicked_cb(self, *args):
		"""
		Handles callback when the reload button is clicked.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__filesaver.reset_save_flag()
		self.__editor.emit("reload-document")
		self.__hide()
		return True

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the window is closed.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.
		"""
		self.__ignore_button.activate()
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "Esc" key is pressed.

		@param self: Reference to the ModificationDialog instance.
		@type self: A ModificationDialog object.

		@param window: Reference to the dialog.
		@type window: A ModificationDialog object.

		@param event: A key press event.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import keysyms
		from operator import ne
		if ne(event.keyval, keysyms.Escape): return False
		self.__ignore_button.activate()
		return True
