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
from gettext import gettext as _
class Window(object):
	"""
	This class defines the behavior of the window for the text editor.
	"""

	def __init__(self, editor, uri):
		self.__init_attributes(editor, uri)
		self.__set_properties()
		self.__sigid1 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid2 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid3 = editor.connect("close", self.__close_cb)
		self.__sigid4 = self.__window.connect("window-state-event", self.__state_event_cb)
		self.__sigid5 = self.__window.connect("focus-out-event", self.__focus_out_event_cb)
		self.__sigid6 = self.__window.connect("focus-in-event", self.__focus_in_event_cb)
		editor.register_object(self)
		self.__position_window()
		self.__window.present()
		self.__window.set_property("sensitive", True)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.gui.get_widget("Window")
		self.__uri = str(uri) if uri else None
		self.__title = self.__set_title()
		self.__is_minimized = False
		self.__is_maximized = False
		return

	def __set_properties(self):
		width, height = self.__editor.calculate_resolution_independence(self.__window, 1.462857143, 1.536)
		self.__window.set_property("default-height", height)
		self.__window.set_property("default-width", width)
		if self.__uri: self.__update_window_title(_('Loading "%s" ...') % self.__title)
		return

	def __update_window_title(self, title):
		self.__window.set_property("title", title)
		return False

	def __set_title(self):
		from gnomevfs import URI
		return URI(self.__uri).short_name.encode("utf-8") if self.__uri else None

	def __position_window(self):
		try:
			uri = self.__uri if self.__uri else "<EMPTY>"
			# Get window position from the position database, if possible.
			from PositionMetadata import get_window_position_from_database
			maximize, width, height, xcoordinate, ycoordinate = \
				get_window_position_from_database(uri)# or \
			if maximize:
				self.__window.maximize()
			else:
				self.__window.resize(width, height)
				self.__window.move(xcoordinate, ycoordinate)
		except TypeError:
			pass
		return False

	def __set_window_position_in_database(self):
		xcoordinate, ycoordinate = self.__window.get_position()
		width, height = self.__window.get_size()
		is_maximized = self.__is_maximized
		uri = self.__uri if self.__uri else "<EMPTY>"
		window_position = (True, None, None, None, None) if is_maximized else (False, width, height, xcoordinate, ycoordinate)
		from PositionMetadata import update_window_position_in_database
		update_window_position_in_database(str(uri), window_position)
		return

	def __destroy(self):
		self.__window.hide()
		self.__editor.disconnect_signal(self.__sigid1, self.__window)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__editor.disconnect_signal(self.__sigid6, self.__window)
		self.__editor.emit("quit")
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

########################################################################
#
#					Signal and Event Callback Handlers
#
########################################################################

	def __delete_event_cb(self, widget, event):
		self.__editor.close()
		return True

	def __focus_out_event_cb(self, window, event):
		# Save a document when the text editor's window loses focus.
#		if self.__editor.uri and self.__editor.file_is_saved is False and self.__editor.is_readonly is False:
#			self.__editor.save_file()
#		if self.__is_quiting: return False
		self.__window.grab_remove()
		self.__set_window_position_in_database()
		return False

	def __focus_in_event_cb(self, *args):
		self.__window.grab_add()
		self.__set_window_position_in_database()
		return False

	def __state_event_cb(self, window, event):
		from gtk.gdk import WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN
		from gtk.gdk import WINDOW_STATE_ICONIFIED
		self.__is_minimized = False
		self.__is_maximized = False
		if not (event.new_window_state in (WINDOW_STATE_ICONIFIED, WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN)): return False
		if (event.new_window_state == WINDOW_STATE_ICONIFIED):
			self.__is_minimized = True
		if event.new_window_state in (WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN):
			self.__is_maximized = True
		return False

	def __key_press_event_cb(self, window, event):
		from gtk.gdk import CONTROL_MASK
		# We only care when the "Ctrl" modifier is pressed.
		if not (event.state &CONTROL_MASK): return False
		from gtk import keysyms
		# We only care when "w" key is pressed.
		if not (event.keyval in (keysyms.W, keysyms.w)): return False
		# Ctrl - w will save window position in database.
		# Ctrl - Shift - W will not save window position in database.
		self.__editor.close(False) if event.keyval == keysyms.W else self.__editor.close()
		return True

	def __close_cb(self, editor, save_file):
		if save_file: self.__set_window_position_in_database()
		self.__destroy()
		return False

	# Public APIs

	maximized = property(lambda self: self.__is_maximized)
	minimized = property(lambda self: self.__is_minimized)
