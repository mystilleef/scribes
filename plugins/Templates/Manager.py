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
This module documents a class that manages components that implement
dynamic templates for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class TemplatesManager(GObject):
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
		"no-trigger-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"trigger-activated": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"template-destroyed": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"next-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"previous-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the TemplatesManager instance.
		@type self: A TemplatesManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__signal_id_1 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TemplatesManager instance.
		@type self: A TemplatesManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Highlighter import Highlighter
		self.__highlighter = Highlighter(self, editor)
		from Monitor import TemplateMonitor
		self.__monitor = TemplateMonitor(self, editor)
		from Loader import TemplateLoader
		self.__loader = TemplateLoader(self, editor)
		from Factory import TemplateFactory
		self.__factory = TemplateFactory(self, editor)
		self.__signal_id_1 = None
		return

	def __destroy_cb(self, manager):
		"""
		Destroy instance of this object.

		@param self: Reference to the TemplatesManager instance.
		@type self: A TemplatesManager object.

		@param manager: Reference to the TemplatesManager instance.
		@type manager: A TemplatesManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		del self
		self = None
		return
