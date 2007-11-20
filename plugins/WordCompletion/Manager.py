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
This module documents a class that implements automatic word completion
for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT, TYPE_OBJECT

class CompletionManager(GObject):
	"""
	This class creates an object that manages objects that provide
	specialized services for word completion and allows the objects
	to communicate with each other via signals.
	"""

	__gsignals__ = {
		"update": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"match-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"no-match-found": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"populated-model": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"is-visible": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__arrange_widgets()
		self.__signal_id_1 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Monitor import CompletionMonitor
		self.__monitor = CompletionMonitor(self, editor)
		from Updater import CompletionUpdater
		self.__updater = CompletionUpdater(self, editor)
		from Window import CompletionWindow
		self.__window = CompletionWindow(self, editor)
		from TreeView import CompletionTreeView
		self.__textview = CompletionTreeView(self, editor)
		from ScrollWin import CompletionScrollWin
		self.__scrollwin = CompletionScrollWin(self)
		self.__signal_id_1 = None
		return

	def __arrange_widgets(self):
		"""
		Arrange widgets in the word completion window.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.
		"""
		self.__scrollwin.add(self.__textview)
		self.__window.add(self.__scrollwin)
		return
		
	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the CompletionManager instance.
		@type self: An CompletionManager object.

		@param manager: Reference to the CompletionManager.
		@type manager: An CompletionManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		del self
		self = None
		return
