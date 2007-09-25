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
This module documents a class that manages key components of the template
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_STRING
from gobject import TYPE_BOOLEAN, TYPE_PYOBJECT

class TemplateManager(GObject):
	"""
	This class creates an object that manages key components of the
	template editor.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"language-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"trigger-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"description-treeview-sensitivity": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"sensitive": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"template-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"importing": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"import-error": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"remove-template": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"export-template": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"imported-language": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, trigger, editor):
		"""
		Initialize object.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.

		@param trigger: An object that shows the template editor.
		@type trigger: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		scroll = self.__glade.get_widget("PreviewScrolledWindow")
		from AddButton import AddButton
		AddButton(self, editor)
		from EditButton import EditButton
		EditButton(self, editor)
		from ExportButton import ExportButton
		ExportButton(self, editor)
		from RemoveButton import RemoveButton
		RemoveButton(self, editor)
		from Preview import Preview
		scroll.add(Preview(self, editor))
		from DescriptionTreeView import DescriptionTreeView
		DescriptionTreeView(self, editor)
		from LanguageTreeView import TemplateLanguageTreeView
		TemplateLanguageTreeView(self, editor)
		from Window import TemplateWindow
		TemplateWindow(self, editor)
		from LinkButton import LinkButton
		LinkButton(self)
		from HelpButton import HelpButton
		HelpButton(self)
		from ImportButton import ImportButton
		ImportButton(self, editor)
		self.__signal_id_1 = trigger.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "Template.glade")
		self.__editor = editor
		from gtk.glade import XML
		self.__glade = XML(glade_file, "TemplateEditorWindow", "scribes")
		self.__signal_id_1 = None
		return

	def __get_glade(self):
		return self.__glade

	glade = property(__get_glade)

	def show(self):
		"""
		Show the template editor.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.
		"""
		self.emit("show")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.

		@param trigger: A trigger to show the template editor.
		@type trigger: A Trigger object.
		"""
		self.emit("destroy")
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, trigger)
		delete_attributes(self)
		self = None
		del self
		return
