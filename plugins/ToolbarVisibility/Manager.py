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
This module documents a class that manages the minimal view mode.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	Creates object that manages minimal view mode.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__sig_id_1 = editor.textview.connect("motion-notify-event", self.__motion_notify_event_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__monitor_mouse, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__timer = self.__sig_id_1 = None
		self.__activate = False
		return

	def __monitor_mouse(self):
		"""
		Enable or disable mouse monitoring.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__disable_mouse_monitor()
		from MinimalModeMetadata import get_value
		if get_value(): self.__enable_mouse_monitor()
		return False

	def __motion_notify_event_cb(self, window, event):
		"""
		Handles callback when the "motion-notify-event" is called.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param window: The text editor window.
		@type window: A gtk.Window object.

		@param event: A gobject event.
		@type event: An gtk.Event object.
		"""
		if self.__activate is False: return False
		window.window.get_pointer()
		self.__show_full_view()
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except TypeError:
			pass
		self.__timer = timeout_add(2500, self.__hide_full_view, priority=2000)
		return False

	def __show_full_view(self):
		"""
		Show full view.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.toolbar.set_no_show_all(False)
		self.__editor.statuscontainer.set_no_show_all(False)
		self.__editor.toolbar.show_all()
		self.__editor.toolbarcontainer.show_all()
		self.__editor.statuscontainer.show_all()
		self.__editor.statuscontainer.set_no_show_all(True)
		self.__editor.toolbar.set_no_show_all(True)
		return False

	def __hide_full_view(self):
		"""
		Hide full view.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.toolbar.set_no_show_all(False)
		self.__editor.statuscontainer.set_no_show_all(False)
		self.__editor.toolbar.hide()
		self.__editor.toolbarcontainer.hide()
		self.__editor.statuscontainer.hide()
		self.__editor.statuscontainer.set_no_show_all(True)
		self.__editor.toolbar.set_no_show_all(True)
		return False

	def __disable_mouse_monitor(self):
		"""
		Don't monitor cursor movement.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.textview.handler_block(self.__sig_id_1)
		self.__activate = False
		return

	def __enable_mouse_monitor(self):
		"""
		Monitor cursor movement.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.textview.handler_unblock(self.__sig_id_1)
		self.__activate = True
		return

	def toggle_minimal_interface(self):
		"""
		Toggle minimal interface.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		from MinimalModeMetadata import get_value, set_value
		minimal_mode = get_value()
		if minimal_mode:
			set_value(False)
			self.__disable_mouse_monitor()
		else:
			set_value(True)
			self.__enable_mouse_monitor()
		return

	def destroy(self):
		"""
		Destroy manager object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__editor.textview)
		del self
		self = None
		return
