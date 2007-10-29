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
This module documents a class that creates the word completion window
for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_OBJECT, TYPE_PYOBJECT

class CompletionManager(GObject):
	"""
	This class creates the word completion window for the text editor.
	The class enables communication between individual components of
	the word completion window.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_OBJECT,)),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"populated-model": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_OBJECT,)),
		"is-visible": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
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
		self.__can_create_widgets()
		self.__signal_id_1 = self.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = editor.store.connect("updated", self.__updated_cb)
		from gobject import timeout_add
		timeout_add(5000, self.__check_completion_object)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__completion = editor.get_object("WordCompletionManager")
		self.__window = None
		self.__textview = None
		self.__scrollwin = None
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __create_widgets(self):
		"""
		Create widgets for the word completion window.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.
		"""
		from Window import CompletionWindow
		self.__window = CompletionWindow(self, self.__editor, self.__completion)
		from TreeView import CompletionTreeView
		self.__textview = CompletionTreeView(self, self.__editor, self.__completion)
		from ScrollWin import CompletionScrollWin
		self.__scrollwin = CompletionScrollWin(self)
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

	def __can_create_widgets(self):
		"""
		Whether or not to create widgets for word completion window.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.
		"""
		from operator import not_
		if not_(self.__completion): return
		self.__create_widgets()
		self.__arrange_widgets()
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __updated_cb(self, store, name):
		"""
		Handles callback when the "updated" signal is emitted.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.

		@param store: Reference to the editor's generic storage object.
		@type store: A Store object.

		@param name: Name of the object that is stored or removed.
		@type name: A String object.
		"""
		from operator import eq
		if eq("WordCompletionManager", name):
			self.__completion = store.get_object("WordCompletionManager")
			self.__can_create_widgets()
		return

	def __check_completion_object(self):
		try:
			if self.__completion: return False
			self.__completion = self.__editor.get_object("WordCompletionManager")
			self.__can_create_widgets()
		except AttributeError:
			pass
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the CompletionManager instance.
		@type self: A CompletionManager object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor.store)
		del self
		self = None
		return
