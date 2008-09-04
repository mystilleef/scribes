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

class Window(object):
	"""
	This class defines the behavior of the window for the text editor.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid2 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid3 = editor.connect("close", self.__close_cb)
		editor.register_object(self)
		self.__window.show_all()
		self.__window.set_property("sensitive", True)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.gui.get_widget("Window")
		return

	def __set_properties(self):
		width, height = self.__editor.calculate_resolution_independence(self.__window, 1.462857143, 1.536)
		self.__window.set_property("default-height", height)
		self.__window.set_property("default-width", width)
		return

	def __destroy(self):
		self.__window.hide()
		self.__editor.disconnect_signal(self.__sigid1, self.__window)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
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
		if save_file: print "Will update database"
		self.__destroy()
		return False
