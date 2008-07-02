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

class Manager(GObject):
	"""
	This class creates an object that manages key components of the
	template editor.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"process": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"language-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"template-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"description-view-sensitivity": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"select-description-view": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-add-dialog": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-edit-dialog": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"dialog-hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"valid-trigger": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"trigger-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"description-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"temp-selected": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"process-1": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"process-2": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-updated": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"remove-templates": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-import-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-import-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-export-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-export-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"import-selected-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"process-imported-files": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"import-button-clicked": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"export-button-clicked": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"valid-xml-templates": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"invalid-xml-templates": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"template-data": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"select-langauge": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"export-template-filename": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"process-templates-for-export": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"processed-template-data": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"get-selected-templates": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		from Editor import Editor
		Editor(self, editor)
		from DialogCancelButton import Button
		Button(self, editor)
		from DialogSaveButton import Button
		Button(self, editor)
		from DialogDescriptionEntry import Entry
		Entry(self, editor)
		from DialogNameEntry import Entry
		Entry(self, editor)
		from DialogWindow import Window
		Window(self, editor)
		from AddButton import Button
		Button(self, editor)
		from RemoveButton import Button
		Button(self, editor)
		from EditButton import Button
		Button(self, editor)
		from TemplateDatabaseUpdater import Updater
		Updater(self, editor)
		from XMLTemplateImporter import Importer
		Importer(self, editor)
		from XMLTemplateValidator import Validator
		Validator(self, editor)
		from ImportDialogImportButton import Button
		Button(self, editor)
		from ImportDialogWindow import Window
		Window(self, editor)
		from ImportDialogFileChooser import FileChooser
		FileChooser(self, editor)
		from ImportDialogCancelButton import Button
		Button(self, editor)
		from ImportButton import Button
		Button(self, editor)
		from TemplateExporter import Exporter
		Exporter(self, editor)
		from XMLTemplateWriter import Writer
		Writer(self, editor)
		from ExportDialogExportButton import Button
		Button(self, editor)
		from ExportDialogFileChooser import FileChooser
		FileChooser(self, editor)
		from ExportDialogWindow import Window
		Window(self, editor)
		from HelpButton import Button
		Button(self, editor)
		from ExportDialogCancelButton import Button
		Button(self, editor)
		from ExportButton import Button
		Button(self, editor)
		from Preview import Preview
		Preview(self, editor)
		from DescriptionTreeView import TreeView
		TreeView(self, editor)
		from LanguageTreeView import TreeView
		TreeView(self, editor)
		from Window import Window
		Window(self, editor)
		from LinkButton import Button
		Button(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		current_folder = editor.get_current_folder(globals())
		glade_file = join(current_folder, "TemplateEditor.glade")
		dialog_file = join(current_folder, "DialogEditor.glade")
		import_dialog_file = join(current_folder, "ImportDialog.glade")
		export_dialog_file = join(current_folder, "ExportDialog.glade")
		self.__editor = editor
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		self.__dglade = XML(dialog_file, "Window", "scribes")
		self.__iglade = XML(import_dialog_file, "Window", "scribes")
		self.__eglade = XML(export_dialog_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	def __get_dglade(self):
		return self.__dglade

	def __get_iglade(self):
		return self.__iglade

	def __get_eglade(self):
		return self.__eglade

	glade = property(__get_glade)
	dglade = property(__get_dglade)
	iglade = property(__get_iglade)
	eglade = property(__get_eglade)

	def show(self):
		self.emit("show-window")
		return

	def destroy(self):
		self.__destroy()
		return

	def __destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
