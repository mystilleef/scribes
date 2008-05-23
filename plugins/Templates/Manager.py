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
This module documents a class that manages components that implement
dynamic templates for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class creates an object that manages other objects that
	implement dynamic templates for the text editor. This class allows
	the helper objects to communicate with each other via signals.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"loaded-language-templates": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"loaded-general-templates": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"trigger-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"no-trigger-found": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"trigger-activated": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"template-destroyed": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"template-boundaries": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"next-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"previous-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"expand-trigger": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"deactivate-template-mode": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"activate-template-mode": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy-template": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"last-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"placeholders": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"tag-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		from TriggerColorer import Colorer
		Colorer(editor, self)
		from TemplateDeactivator import Deactivator
		Deactivator(editor, self)
		from PlaceholderColorer import Colorer
		Colorer(editor, self)
		from PlaceholderNavigator import Navigator
		Navigator(editor, self)
		from TriggerMonitor import Monitor
		Monitor(editor, self)
		from TemplateInserter import Inserter
		Inserter(editor, self)
		from Loader import Loader
		Loader(editor, self)

	def __destroy(self):
		"""
		Destroy this object and subordinate objects it manages.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.emit("destroy")
		del self
		self = None
		return

	def destroy(self):
		"""
		Destroy object and subordinate objects it manages.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__destroy()
		return
