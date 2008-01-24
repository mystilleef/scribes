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
This module documents a class that creates a window to allow users open
files with a specified encoding.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class EncodingErrorWindow(object):
	"""
	This class implements a window that allows users to open documents
	in a specific encoding.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__add_combobox()
		self.__sig_id_1 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sig_id_2 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sig_id_3 = self.__open_button.connect("clicked", self.__open_clicked_cb)
		self.__sig_id_4 = self.__close_button.connect("clicked", self.__close_clicked_cb)
		self.__sig_id_5 = editor.connect("close-document", self.__destroy_cb)
		self.__sig_id_6 = editor.connect("close-document-no-save", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize object's attributes.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.scribes_data_folder, "EncodingErrorWindow.glade")
		from gtk.glade import XML
		glade = XML(glade_file, "Window")
		self.__window = glade.get_widget("Window")
		self.__hbox = glade.get_widget("HBox")
		self.__label = glade.get_widget("TitleLabel")
		self.__open_button = glade.get_widget("OpenButton")
		self.__close_button = glade.get_widget("CloseButton")
		self.__uri = None
		from EncodingComboBox import EncodingComboBox
		self.__combobox = EncodingComboBox(editor)
		return

	def show_message(self, title, uri):
		"""
		Show error dialog.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.

		@param title: Title of the window.
		@type title: A String object.

		@param uri: Name of the file.
		@type uri: A String object.
		"""
		self.__uri = uri
		self.__label.set_label(title)
		self.__show()
		return

	def __add_combobox(self):
		"""
		Add combobox to window.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__hbox.pack_start(self.__combobox, True, True, 0)
		return

	def __show(self):
		"""
		Show window.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__window.show_all()
		return

	def __hide(self):
		"""
		Hide window.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__uri = None
		self.__window.hide()
		return

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__window)
		self.__editor.disconnect_signal(self.__sig_id_2, self.__window)
		self.__editor.disconnect_signal(self.__sig_id_3, self.__open_button)
		self.__editor.disconnect_signal(self.__sig_id_4, self.__close_button)
		self.__editor.disconnect_signal(self.__sig_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__sig_id_6, self.__editor)
		self.__window.destroy()
		del self
		self = None
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the "delete-event" signal is emitted.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__hide()
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" is emitted.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		# Hide window when escape key is pressed.
		from gtk import keysyms
		from operator import eq
		if eq(event.keyval, keysyms.Escape): self.__hide()
		return False

	def __close_clicked_cb(self, *args):
		"""
		Handles callback when the button's "clicked" signal is emitted.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__hide()
		return False

	def __open_clicked_cb(self, *args):
		"""
		Handles callback when the button's "clicked" signal is emitted.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__editor.load_uri(self.__uri, self.__combobox.encoding)
		self.__hide()
		return False

	def __destroy_cb(self, *args):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the EncodingErrorWindow instance.
		@type self: An EncodingErrorWindow object.
		"""
		self.__destroy()
		return False
