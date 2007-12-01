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
This module implements a class responsible for creating a window object for
text editor instances.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Window

class ScribesWindow(Window):
	"""
	This class creates the window for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the text editor's window instance.
		@type self: A ScribesWindow object.
		"""
		self.__precompile_methods()
		Window.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = self.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_2 = self.connect("map-event", self.__map_event_cb, editor)
		self.__signal_id_3 = self.connect("window-state-event", self.__state_event_cb)
		self.__signal_id_4 = self.__editor.connect("gui-created", self.__gui_created_cb)
		self.__signal_id_5 = self.__editor.connect("loading-document", self.__loading_document_cb)
		self.__signal_id_6 = self.__editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_7 = self.__editor.connect("load-error", self.__load_error_cb)
		self.__signal_id_8 = self.__editor.connect("enable-readonly", self.__enable_readonly_cb)
		self.__signal_id_9 = self.__editor.connect("disable-readonly", self.__disable_readonly_cb)
		self.__signal_id_10 = self.__editor.connect_after("saved-document", self.__saved_document_cb)
		self.__signal_id_11 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_12 = self.__editor.connect("enable-fullscreen", self.__enable_fullscreen_cb)
		self.__signal_id_13 = self.__editor.connect("disable-fullscreen", self.__disable_fullscreen_cb)
		self.__signal_id_14 = self.__editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_15 = self.__editor.connect("hide-bar", self.__hide_bar_cb)
		self.__signal_id_16 = self.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_17 = self.connect_after("focus-out-event", self.__focus_out_event_cb)
		self.__signal_id_19 = self.__editor.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_20 = self.__editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_21 = self.__editor.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_22 = self.__editor.connect("buffer-created", self.__created_widgets_cb)
		self.__signal_id_23 = self.__editor.connect("reload-document", self.__reload_document_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the text editor's window attributes.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.
		"""
		self.__editor = editor
		self.__title = None
		self.__bar_is_visible = False
		self.__bar = None
		self.__is_fullscreen = False
		# The flag is used to indicate whether or not the window is been mapped
		# to screen for the first time. The flag is True if it is been mapped
		# to screen for the first time, and False otherwise.
		self.__is_first_time = True
		# True if the window has been drawn to screen, mapped.
		self.__is_mapped = False
		# True if the window is maximized.
		self.__is_maximized = False
		self.__window_position_timer = None
		self.__uri = None
		self.__positioned = False
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = self.__signal_id_11 = self.__signal_id_12 = None
		self.__signal_id_13 = self.__signal_id_14 = self.__signal_id_15 = None
		self.__signal_id_16 = self.__signal_id_17 = self.__signal_id_18 = None
		self.__signal_id_19 = self.__signal_id_20 = self.__signal_id_21 = None
		self.__signal_id_22 = None
		# Register a unique number with the editor's termination queue
		self.__termination_id = editor.register_object()
		return

	def __get_is_maximized(self):
		return self.__is_maximized

	def __get_is_fullscreen(self):
		return self.__is_fullscreen

	is_maximized = property(__get_is_maximized)
	is_fullscreen = property(__get_is_fullscreen)

	def __set_properties(self):
		"""
		Set the default text editor's window properties.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.
		"""
		width, height = self.__editor.calculate_resolution_independence(self, 1.462857143,
															1.536)
		from internationalization import msg0025
		self.set_property("title", msg0025)
		self.set_property("icon-name", "scribes")
		self.set_property("default-height", height)
		self.set_property("default-width", width)
		self.set_property("role", "main_window")
		self.set_property("urgency-hint", True)
		self.set_property("border-width", 1)
		self.set_property("name", "EditorWindow")
		self.set_focus_on_map(True)
		return

########################################################################
#
#					Signal and Event Callback Handlers
#
########################################################################

	def __delete_event_cb(self, widget, event):
		"""
		Handles callback the "delete-event" signal is emitted.

		This function quits the text editor.

		@param self: Reference to the text editor's instance.
		@type self: A ScribesWindow object.

		@param widget: Reference to the text editor's instance.
		@type widget: A gtk.Window object.

		@param event: An event to destroy a window object.
		@type event: A gtk.Event object.

		@param editor: Reference to the text editor instance.
		@type editor: An Editor object.

		@return: True to prevent propagation of the signal to parent widgets.
		@rtype: A Boolean object.
		"""
		self.__editor.trigger("close_window")
		return True

	def __map_event_cb(self, widget, event, editor):
		"""
		Handles callback when the "map-event" signal is emitted.

		If the text editor's window is displayed for the first time, this
		function binds the text editor's accelerators to the window and resizes
		children widgets.

		@param self: Reference to the text editor's instance.
		@type self: A ScribesWindow object.

		@param widget: Reference to the text editor's instance.
		@type widget: A gtk.Window object.

		@param event: An event that shows the editor window.
		@type event: A gtk.Event object.

		@return: True to prevent propagation of the signal to parent widgets.
		@rtype: A Boolean object.
		"""
		if self.__is_first_time:
			self.__is_first_time = False
			self.__is_mapped = True
		return True

	def __focus_out_event_cb(self, window, event):
		"""
		Handles callback when the "focus-out-event" signal is emitted.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param window: The text editor's window.
		@type window: A ScribesWindow object.

		@param event: An event that occurs when the window looses focus.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		# Save a document when the text editor's window loses focus.
		if self.__editor.uri and self.__editor.file_is_saved is False and self.__editor.is_readonly is False:
			self.__editor.trigger("save_file")
		from gtk.gdk import flush
		flush()
		return False

	def __state_event_cb(self, window, event):
		"""
		Handles callback when the "window-state-event" is emitted.

		This function keeps track of the state of the window.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param window: Reference to the text editor window.
		@type window: A gtk.Window object.

		@param event: An event that shows the editor window.
		@type event: A gtk.Event object.

		@return: True to prevent propagation of the signal to parent widgets.
		@rtype: A Boolean object.
		"""
		from operator import eq, contains
		from gtk.gdk import WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN
		from gtk.gdk import WINDOW_STATE_ICONIFIED
		if eq(event.new_window_state, WINDOW_STATE_ICONIFIED): return False
		self.__is_maximized = False
		if contains((WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN), event.new_window_state):
			self.__is_maximized = True
		return False

	def __loading_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor is in the process of loading a
		document.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.__uri = uri
		# Set the titlebar to show the file is currently being loaded.
		self.__determine_title(uri)
		from internationalization import msg0335
		self.set_title(msg0335 % self.__title)
		return

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor has finished loading a document.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		#self.__editor.textbuffer.handler_unblock(self.__signal_id_18)
		self.__editor.handler_unblock(self.__signal_id_18)
		self.__uri = uri
		self.set_title(self.__title)
		self.show_all()
		self.present()
		return

	def __load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		This function is called when an error occurs while loading a document.
		The function quits the text editor, if the an error occurs before the
		text editor window is displayed. This is done to prevent the text
		editor's process from running indefinitely.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		#self.__editor.textbuffer.handler_unblock(self.__signal_id_18)
		self.__editor.handler_unblock(self.__signal_id_18)
		from internationalization import msg0025
		self.__uri = None
		self.__title = None
		self.set_title(msg0025)
		if self.__is_mapped is False: self.__editor.emit("close-document-no-save")
		return

	def __checking_document_cb(self, editor, uri):
		self.__uri = uri
		#self.__editor.textbuffer.handler_block(self.__signal_id_18)
		self.__editor.handler_block(self.__signal_id_18)
		# Set the titlebar to show the file is currently being loaded.
		self.__determine_title(uri)
		from internationalization import msg0335
		self.set_title(msg0335 % self.__title)
		self.__position_window()
		return

	def __enable_readonly_cb(self, editor):
		"""
		Handles callback when the text editor is in readonly mode.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		from internationalization import msg0034
		self.set_title(self.__title + msg0034)
		return

	def __disable_readonly_cb(self, editor):
		"""
		Handles callback when the "disable-readonly" signal is emitted.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_title(self.__title)
		return

	def __gui_created_cb(self, editor):
		"""
		Handles callback when the "gui-created" signal is emitted.

		This function displays the text editor on the screen.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		if self.__editor.will_load_document: return
		self.__show_window()
		return

	def __created_widgets_cb(self, editor):
		#self.__signal_id_18 = self.__editor.textbuffer.connect("changed", self.__changed_cb)
		self.__signal_id_18 = self.__editor.connect_after("modified-document", self.__changed_cb)
		return

	def __changed_cb(self, textbuffer):
		"""
		Handles callback when the text editor's buffer "changed" signal is
		emitted.

		This function prepends an asterik to the name of the document in the
		titebar, when text is entered in the text editor's buffer.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param textbuffer: Reference to the text editor's buffer.
		@type textbuffer: A gtksourceview.SourceBuffer object.

		@return: True to propagate signals to parent widgets.
		@rtype: A Boolean object.
		"""
		if not self.__uri: return True
		from operator import eq
		if eq(self.get_title(), self.__title): self.set_title("*" + self.__title)
		return True

	def __enable_fullscreen_cb(self, editor):
		"""
		Handles callback when the "enable-fullscreen" signal is emitted.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__is_fullscreen = True
		self.fullscreen()
		return

	def __disable_fullscreen_cb(self, editor):
		"""
		Handles callback when "disable-fullscreen" signal is emitted.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__is_fullscreen = False
		self.unfullscreen()
		return

	def __show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The bar for the text editor.
		@type bar: A ScribesBar object.
		"""
		self.__bar = bar
		self.__bar_is_visible = True
		return

	def __hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The bar for the text editor.
		@type bar: A ScribesBar object.
		"""
		self.__bar_is_visible = False
		return

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		This function hides the text editor's bar.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param window: The text editor's window.
		@type window: A ScribesWindow object.

		@param event: An event that happens when the keyboard keys are pressed.
		@type event: A gtk.Event object.

		@param bar: The bar for the text editor.
		@type bar: A ScribesBar object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		editor = self.__editor
		from gtk import keysyms
		if event.keyval == keysyms.Escape and self.__bar_is_visible:
			self.__bar.hide_bar()
			return True
		if event.keyval == keysyms.Escape and self.__uri is None and editor.contains_document is False:
			editor.trigger("close_window")
		from gtk.gdk import CONTROL_MASK, SHIFT_MASK
		if event.state & CONTROL_MASK and event.state & SHIFT_MASK:
			if event.keyval == keysyms.W and self.__uri is None:
				self.hide_all()
				editor.emit("close-document-no-save")
		return False

	def __show_window(self):
		"""
		Show the text editor's window.

		When the text editor is loading a document, the window is shown only
		after metadata information about the document's most recent window size
		and position have retrieved from the position database. This information
		is used to calculate the documents window position and size before
		displaying it.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		self.__position_window()
		self.show_all()
		from gtk.gdk import notify_startup_complete
		notify_startup_complete()
		return False

	def __position_window(self):
		"""
		Show the text editor's window.

		When the text editor is loading a document, show the window after
		metadata information about the document's most recent window size and
		position has been retrieved.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.
		"""
		try:
			if not self.__uri: return False
			# Get window position from the position database, if possible.
			from position_metadata import get_window_position_from_database
			maximize, width, height, xcoordinate, ycoordinate = \
				get_window_position_from_database(self.__uri)
			if maximize:
				self.maximize()
			else:
				if self.__is_mapped is False:
					self.move(xcoordinate, ycoordinate)
				self.resize(width, height)
		except TypeError:
			pass
		return False

	def __saved_document_cb(self, editor, uri):
		"""
		Handles callback when the contents of the text editor's buffer have
		been saved.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor's buffer.
		@type editor: An Editor object.
		"""
		self.set_title(self.__title)
		return False

	def __close_document_cb(self, editor):
		"""
		Record metadata information about the text editor's window and hide it.

		This function gets the window's position and size, records the
		information in a metadata database, and then hides the text editor's
		window.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param editor: An instance of the text editor's buffer.
		@type editor: An Editor object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_17, self)
		# Get the text editor's window size and position.
		xcoordinate, ycoordinate = self.get_position()
		width, height = self.get_size()
		is_maximized = self.__is_maximized
		# Update the metadata database with the size and position of the window.
		from gobject import idle_add
		idle_add(self.__update_position_metadata, is_maximized, xcoordinate, ycoordinate, width, height)
		self.hide_all()
		return False

	def __close_document_no_save_cb(self, editor):
		self.__editor.disconnect_signal(self.__signal_id_17, self)
		self.__destroy()
		return False

	def __renamed_document_cb(self, editor, uri):
		self.__uri = uri
		self.__determine_title(self.__uri)
		self.set_title(self.__title)
		return False

	def __reload_document_cb(self, *args):
		from internationalization import msg0489
		message = msg0489 % (self.__uri)
		self.set_title(message)
		return False

########################################################################
#
#					Metadata Information Management
#
########################################################################

	def __update_position_metadata(self, is_maximized, xcoordinate, ycoordinate, width, height):
		"""
		Update the position database with information about the text editor's
		window position.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param uri: A universal resource identifier representing, or pointing
			to, a text document.
		@type uri: A String object.
		"""
		self.__stop_window_position_timer()
		from position_metadata import update_window_position_in_database
		if self.__uri:
			if is_maximized:
				window_position = (True, None, None, None, None)
				update_window_position_in_database(str(self.__uri), window_position)
			else:
				window_position = (False, width, height, xcoordinate, ycoordinate)
				update_window_position_in_database(str(self.__uri), window_position)
		self.__destroy()
		return False

	def __stop_window_position_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__window_position_timer)
		except:
			pass
		return

	def __determine_title(self, uri):
		from gnomevfs import URI
		self.__title = URI(uri).short_name.encode("utf-8")
		return False

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__key_press_event_cb)
		except ImportError:
			pass
		return False

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_17, self)
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		self.__editor.disconnect_signal(self.__signal_id_16, self)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_11, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_12, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_13, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_14, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_15, self.__editor)
		#self.__editor.disconnect_signal(self.__signal_id_18, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__signal_id_18, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_19, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_20, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_21, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_22, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_23, self.__editor)
		self.__editor.unregister_object(self.__termination_id)
		del self
		self = None
		return
