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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module exposes a class used to create statusbar objects for the text
editor. The statusbar object are customized for the text editor.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Statusbar

class ScribesStatusbar(Statusbar):
	"""
	This class creates instances of statusbar objects for the text editor.
	"""

	def __init__(self, editor):
		Statusbar.__init__(self)
		self.__init_attributes(editor)
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__registration_id = editor.register_object()
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __destroy(self):
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.destroy()
		# Unregister object so that editor can quit.
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return

	def __close_document_cb(self, editor):
		self.__destroy()
		return

class StatusOne(ScribesStatusbar):

	def __init__(self, editor):
		ScribesStatusbar.__init__(self, editor)
		self.editor = editor
		self.set_has_resize_grip(False)
		# Initialize the first statusbar context identification.
		self.context_id = 0
		self.text = None
		self.connect("text-popped", self.__statusone_text_popped_cb)
		self.connect("text-pushed", self.__statusone_text_pushed_cb)

	def __statusone_text_popped_cb(self, statusbar, context_id, text):
		self.context_id = context_id
		self.text = text
		return False

	def __statusone_text_pushed_cb(self, statusbar, context_id, text):
		self.context_id = context_id
		self.text = text
		return False

class StatusTwo(ScribesStatusbar):

	def __init__(self, editor):
		ScribesStatusbar.__init__(self, editor)
		self.editor = editor
		self.__id = None
		self.__is_updating = False
		self.set_property("width-request", 160)
		self.set_has_resize_grip(False)
		# Initialize the second statusbar context identification.
		self.context_id = 0
		self.editor.connect("gui-created", self.__statustwo_gui_created_cb)
		self.editor.connect("enable-readonly", self.__statustwo_enable_readonly_cb)
		self.editor.connect("disable-readonly", self.__statustwo_disable_readonly_cb)

	def __statustwo_gui_created_cb(self, editor):
		# Update the cursor position on the statusbar.
		from gobject import idle_add, PRIORITY_LOW
		self.__stop_idle_add()
		self.__id = idle_add(self.__update_cursor_position, editor.textview, priority=PRIORITY_LOW)
		editor.connect("cursor-moved", self.__statustwo_cursor_moved_cb)
		return

	def __statustwo_cursor_moved_cb(self, editor):
		# Update the cursor position on the statusbar.
		from gobject import idle_add, timeout_add, PRIORITY_LOW
		self.__stop_idle_add()
		self.__id = timeout_add(500, self.__update_cursor_position, editor.textview, priority=5555)
		return

	def __stop_idle_add(self):
		try:
			from gobject import source_remove
			source_remove(self.__id)
		except:
			pass
		return

	def __update_cursor_position(self, textview):
		try:
			if self.__is_updating: return False
			self.__is_updating = True
			from cursor import update_cursor_position
			update_cursor_position(self, textview)
		except AttributeError:
			pass
		except RuntimeError:
			pass
		self.__is_updating = False
		return False

	def __statustwo_enable_readonly_cb(self, editor):
		self.hide_all()
		return

	def __statustwo_disable_readonly_cb(self, editor):
		self.show_all()
		return

class StatusThree(ScribesStatusbar):

	def __init__(self, editor):
		ScribesStatusbar.__init__(self, editor)
		self.editor = editor
		self.set_has_resize_grip(True)
		self.set_property("width-request", 80)
		# Let status bar reflect correct textview mode
		from internationalization import msg0354
		self.context_id  = self.get_context_id(msg0354)
		self.push(self.context_id, msg0354)
		self.editor.connect("gui-created", self.__statusthree_gui_created_cb)
		self.editor.connect("enable-readonly", self.__statusthree_enable_readonly_cb)
		self.editor.connect("disable-readonly", self.__statusthree_disable_readonly_cb)

	def __statusthree_gui_created_cb(self, editor):
		editor.textview.connect("toggle-overwrite", self.__statusthree_toggle_overwrite_cb)
		return

	def __statusthree_toggle_overwrite_cb(self, textview):
		# Set textview overwrite mode
		if not textview.get_overwrite():
			from internationalization import msg0355
			mode = msg0355
		else:
			from internationalization import msg0354
			mode = msg0354
		# Let status bar reflect correct textview mode
		self.pop(self.context_id)
		self.context_id = self.get_context_id(mode)
		self.push(self.context_id, mode)
		return False

	def __statusthree_enable_readonly_cb(self, editor):
		self.hide_all()
		return

	def __statusthree_disable_readonly_cb(self, editor):
		self.show_all()
		return
