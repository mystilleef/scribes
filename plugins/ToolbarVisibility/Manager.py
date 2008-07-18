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
		self.__init_attributes(editor)
		self.__sig_id_1 = editor.textview.connect("motion-notify-event", self.__motion_notify_event_cb)
		self.__sig_id_2	= editor.window.connect("leave-notify-event", self.__hide_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__monitor_mouse, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__activate = False
		self.__show = None
		return

	def __monitor_mouse(self):
		self.__disable_mouse_monitor()
		from MinimalModeMetadata import get_value
		if get_value(): self.__enable_mouse_monitor()
		return False

	def __show_hide_full_view(self, widget):
		if self.__activate is False: return False
		x, y, type_ = widget.window.get_pointer()
		if y <= 11:
			if self.__show is True: return False
			self.__show_full_view()
		else:
			if self.__show is False: return False
			self.__hide_full_view()
		return False

	def __generic_cb(self, *args):
		self.__show_hide_full_view(self.__editor.textview)
		return

	def __hide_cb(self, window, event):
		if self.__activate is False: return False
		if not self.__show: return False
		window.window.get_pointer()
		self.__hide_full_view()
		return False

	def __motion_notify_event_cb(self, window, event):
		if self.__activate is False: return False
		self.__show_hide_full_view(window)
		return False

	def __show_full_view(self):
		self.__editor.toolbar.set_no_show_all(False)
		self.__editor.statuscontainer.set_no_show_all(False)
		self.__editor.toolbar.show_all()
		self.__editor.toolbarcontainer.show_all()
		self.__editor.statuscontainer.show_all()
		self.__editor.statuscontainer.set_no_show_all(True)
		self.__editor.toolbar.set_no_show_all(True)
		self.__show = True
		return False

	def __hide_full_view(self):
		self.__editor.toolbar.set_no_show_all(False)
		self.__editor.statuscontainer.set_no_show_all(False)
		self.__editor.toolbar.hide()
		self.__editor.toolbarcontainer.hide()
		self.__editor.statuscontainer.hide()
		self.__editor.statuscontainer.set_no_show_all(True)
		self.__editor.toolbar.set_no_show_all(True)
		self.__show = False
		return False

	def __disable_mouse_monitor(self):
		self.__editor.textview.handler_block(self.__sig_id_1)
		self.__editor.window.handler_block(self.__sig_id_2)
		self.__activate = False
		return

	def __enable_mouse_monitor(self):
		self.__editor.textview.handler_unblock(self.__sig_id_1)
		self.__editor.window.handler_unblock(self.__sig_id_2)
		self.__activate = True
		return

	def toggle_minimal_interface(self):
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
		self.__editor.disconnect_signal(self.__sig_id_1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sig_id_2, self.__editor.window)
		del self
		self = None
		return
