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
		"""
		Initialize a statusbar objects for the text editor and set its
		properties.

		@param self: Reference to the ScribesStatusbar instance.
		@type self: A ScribesStatusbar object.

		@param width: The width size of the statusbar object.
		@type width: An Integer object.

		@param height: The height size of the statusbar object.
		@type height: An Integer object.
		"""
		Statusbar.__init__(self)
		self.__init_attributes(editor)
		self.set_reallocate_redraws(False)
		self.set_redraw_on_allocate(False)
		from gtk import RESIZE_PARENT
		self.set_property("resize-mode", RESIZE_PARENT)
		self.resize_children()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the ScribesMainContainer instance.
		@type self: A ScribesMainContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__registration_id = editor.register_object()
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
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
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__destroy()
		return

class StatusOne(ScribesStatusbar):
	"""
	The class instantiates a statusbar object for the text editor that informs
	the user of the status of the text editor or the operations they are
	currently performing.
	"""

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
		"""
		Handles callback when messages are removed from the statusbar.

		@param self: Reference to the StatusOne instance.
		@type self: A StatusOne object.

		@param statusbar: The first statusbar object for the text editor.
		@type statusbar: A gtk.Statusbar object.

		@param context_id: A number associated with a message on the statusbar.
		@type context_id: An Integer object.

		@param text: The message removed from the statusbar.
		@type text: A String object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.context_id = context_id
		self.text = text
		return True

	def __statusone_text_pushed_cb(self, statusbar, context_id, text):
		"""
		@param self: Reference to the StatusOne instance.
		@type self: A StatusOne object.

		@param statusbar: The first statusbar object for the text editor.
		@type statusbar: A gtk.Statusbar object.

		@param context_id: A number associated with a message on the statusbar.
		@type context_id: An Integer object.

		@param text: The message removed from the statusbar.
		@type text: A String object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.context_id = context_id
		self.text = text
		return True

class StatusTwo(ScribesStatusbar):
	"""
	This class instantiates the second statusbar object of the text editor. This
	statusbar bar displays the position of the cursor in the text editor's
	buffer in real time.
	"""

	def __init__(self, editor):
		ScribesStatusbar.__init__(self, editor)
		self.editor = editor
		self.__id = None
		self.set_property("width-request", 160)
		self.set_has_resize_grip(False)
		# Initialize the second statusbar context identification.
		self.context_id = 0
		self.editor.connect("gui-created", self.__statustwo_gui_created_cb)
		self.editor.connect("enable-readonly", self.__statustwo_enable_readonly_cb)
		self.editor.connect("disable-readonly", self.__statustwo_disable_readonly_cb)

	def __statustwo_gui_created_cb(self, editor):
		"""
		Handles callback when the "gui-created" signal is emitted

		@param self: Reference to the StatusTwo instance.
		@type self: An StatusTwo object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		# Update the cursor position on the statusbar.
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__update_cursor_position, editor.textview, priority=PRIORITY_LOW)
		editor.connect("cursor-moved", self.__statustwo_cursor_moved_cb)
		return

	def __statustwo_cursor_moved_cb(self, editor):
		"""
		Handles callback when the editor's buffer's "mark-set" signal is emitted.

		This function updates the cursor position and reflects the changes of
		the statusbar.

		@param self: Reference to the StatusTwo instance.
		@type self: A StatusTwo object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		# Update the cursor position on the statusbar.
		from gobject import idle_add, PRIORITY_LOW
		self.__stop_idle_add()
		self.__id = idle_add(self.__update_cursor_position, editor.textview, priority=PRIORITY_LOW)
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
			from cursor import update_cursor_position
			update_cursor_position(self, textview)
		except AttributeError:
			pass
		return False

	def __statustwo_enable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readonly" signal is emitted.

		@param self: Reference to the StatusTwo instance.
		@type self: A StatusTwo object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.hide_all()
		return

	def __statustwo_disable_readonly_cb(self, editor):
		"""
		Handles callback when the "disable-readonly" signal is emitted.

		@param self: Reference to the StatusTwo instance.
		@type self: A StatusTwo object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.show_all()
		return

class StatusThree(ScribesStatusbar):
	"""
	This class instantiates the third statusbar object of the text editor. This
	statusbar indicates whether the text editor is in "insert", or "overwrite"
	mode.
	"""

	def __init__(self, editor):
		"""
		Initialize the third statusbar object of the text editor.

		@param self: Reference to the StatusThree instance.
		@type self: A StatusThree object.
		"""
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
		"""
		Handles callback when the "gui-created" signal is emitted

		@param self: Reference to the StatusTwo instance.
		@type self: An StatusTwo object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.textview.connect("toggle-overwrite", self.__statusthree_toggle_overwrite_cb)
		return

	def __statusthree_toggle_overwrite_cb(self, textview):
		"""
		Handles callback when the textview's "toggle-overwrite" signal is
		emitted.

		@param self: Reference to the StatusThree instance.
		@type self: A StatusThree object.

		@param textview: The text editor's buffer container, view.
		@type textview: A gtksourceview.SourceView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
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
		return True

	def __statusthree_enable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readonly" signal is emitted.

		@param self: Reference to the StatusThree instance.
		@type self: A StatusThree object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.hide_all()
		return

	def __statusthree_disable_readonly_cb(self, editor):
		"""
		Handles callback when the "disable-readonly" signal is emitted.

		@param self: Reference to the StatusThree instance.
		@type self: A StatusThree object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.show_all()
		return
