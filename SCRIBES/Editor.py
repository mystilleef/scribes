# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or
# modify it under the # terms of the GNU General Public
# License as published by the Free Software Foundation;
# either version 2 of the License, or (at your option) any
# later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.	See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with # Scribes; if not, write to the Free
# Software Foundation, Inc., 51 Franklin St, ifth Floor,
# Boston, MA  02110-1301  USA

"""
This module exposes a class responsible for creating the graphic user
interface components of the text editor. The class also manages state
information about text editor instances.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_OBJECT, TYPE_PYOBJECT
from gobject import SIGNAL_RUN_FIRST, SIGNAL_ACTION, SIGNAL_RUN_CLEANUP, SIGNAL_NO_RECURSE

class Editor(GObject):
	"""
	This class creates the graphic user interface for the text editor.
	It also exposes APIs that allow third parties to interact with
	key components of the text editor. See the "Public APIs" section
	of this module for APIs you can use to manipulate the editor.
	"""

	__gsignals__ = {
		"checking-document": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"loading-document": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"loaded-document": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT, TYPE_PYOBJECT)),
		"reload-document": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"load-error": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"enable-readonly": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"disable-readonly": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"saving-document": (SIGNAL_ACTION|SIGNAL_RUN_FIRST|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_PYOBJECT,)),
		"saved-document": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_PYOBJECT, TYPE_PYOBJECT)),
		"save-document": (SIGNAL_ACTION|SIGNAL_RUN_FIRST|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-error": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_PYOBJECT,)),
		"gui-created": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-dialog": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_OBJECT,)),
		"hide-dialog": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_OBJECT,)),
		"renamed-document": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_PYOBJECT, TYPE_PYOBJECT)),
		"modified-document": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, ()),
		"close-document": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"close-document-no-save": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"created-widgets": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"enable-fullscreen": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"disable-fullscreen": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"not-yet-implemented": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-bar": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_OBJECT,)),
		"hide-bar": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_OBJECT,)),
		"updated-template-database": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, ()),
		"cursor-moved": (SIGNAL_ACTION|SIGNAL_RUN_CLEANUP|SIGNAL_NO_RECURSE, TYPE_NONE, ()),
		"initialized-trigger-manager": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"initialized-attributes": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"rename-document": (SIGNAL_ACTION|SIGNAL_RUN_FIRST|SIGNAL_NO_RECURSE, TYPE_NONE, (TYPE_PYOBJECT, TYPE_PYOBJECT)),
		"buffer-created": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"started-core-services": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, manager, file_uri=None, encoding=None):
		"""
		Initialize the object.

		@param self: Reference to this editor instance.
		@type self: An Editor object.

		@param manager: An object that manages editor instances.
		@type manager: An EditorManager object.

		@param file_uri: A file to open.
		@param type: A String object.
		"""
		GObject.__init__(self)
		self.__signal_id_1 = self.connect("initialized-attributes", self.__initialized_attributes_cb)
		self.__signal_id_2 = self.connect("created-widgets", self.__created_widgets_cb)
		self.__signal_id_3 = self.connect_after("gui-created", self.__gui_created_after_cb)
		self.__signal_id_4 = self.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_5 = self.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_6 = self.connect("load-error", self.__load_error_cb)
		self.__signal_id_7 = self.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_8 = self.connect("modified-document", self.__modified_document_cb)
		self.__signal_id_9 = self.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_10 = self.connect("enable-readonly", self.__enable_readonly_cb)
		self.__signal_id_11 = self.connect("disable-readonly", self.__disable_readonly_cb)
		self.__signal_id_12 = self.connect("rename-document", self.__rename_document_cb)
		self.__signal_id_13 = self.connect_after("created-widgets", self.__created_widgets_after_cb)
		self.__signal_id_14 = self.connect_after("reload-document", self.__reload_document_cb)
		self.__signal_id_15 = self.connect("started-core-services", self.__started_core_services_cb)
#		self.connect_after("loaded-document", self.__loaded_document_after_cb)
		from gobject import idle_add, PRIORITY_HIGH, PRIORITY_LOW
		idle_add(self.__init_attributes, manager, file_uri, encoding, priority=PRIORITY_HIGH)
		idle_add(self.__precompile_methods, priority=5000)

########################################################################
#
#						Getters for public APIs
#
########################################################################

	def __get_error_dialog(self):
		"""
		Return the error dialog for the text editor.

		@param self: Reference to the text editor.
		@type self: An Editor object.

		@return: An error dialog object for the text editor.
		@rtype: A ScribesErrorDialog object.
		"""
		return self.__error_dialog

	def __get_message_dialog(self):
		"""
		Return the error dialog for the text editor.

		@param self: Reference to the text editor.
		@type self: An Editor object.

		@return: An error dialog object for the text editor.
		@rtype: A ScribesErrorDialog object.
		"""
		return self.__message_dialog

	def __get_tooltip(self):
		"""
		Return the tooltip object for the text editor.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@return: A tooltip object.
		@rtype: A gtk.Tooltip object.
		"""
		return self.__tip

	def __get_preference_menu(self):
		"""
		Return the preference menu for the toolbar.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.

		@return: Preference menu for the toolbar.
		@rtype: A PreferenceMenu object.
		"""
		return self.__preference_menu

	def __get_recent_manager(self):
		return self.__recent_manager

	def __get_recent_menu(self):
		return self.__recent_menu

	def __get_store(self):
		return self.__store

	def __get_instance_manager(self):
		return self.__instance_manager

	def __get_trigger_manager(self):
		return self.__trigger_manager

	def __get_feedback(self):
		return self.__feedback

	def __get_maincontainer(self):
		return self.__maincontainer

	def __get_toolbarcontainer(self):
		return self.__toolbarcontainer

	def __get_viewcontainer(self):
		return self.__viewcontainer

	def __get_statuscontainer(self):
		return self.__statuscontainer

	def __get_window(self):
		return self.__window

	def __get_toolbar(self):
		return self.__toolbar

	def __get_textview(self):
		return self.__textview

	def __get_textbuffer(self):
		return self.__textbuffer

	def __get_will_load_documents(self):
		if self.__file_uri: return True
		return False

	def __get_uri(self):
		return self.__uri

	def __get_encoding(self):
		return self.__encoding_manager.encoding

	def __get_encoding_list(self):
		return self.__encoding_manager.encoding_list

	def __get_encoding_guess_list(self):
		return self.__encoding_manager.encoding_guess_list

	def __get_file_is_saved(self):
		return self.__file_is_saved

	def __get_is_readonly(self):
		return self.__is_readonly

	def __get_contains_document(self):
		return self.__contains_document

	def __get_gconf_client(self):
		"""
		Function is deprecated.
		"""
		# This function is deprecated
		return None

	def __get_status_image(self):
		return self.__status_image

	def __get_status_image_frame(self):
		return self.__status_image_frame

	def __get_response(self):
		return self.__response

	def __get_statusone(self):
		return self.__statusone

	def __get_can_load_file(self):
		return self.__can_load_file

	def __get_id(self):
		return self.__id

	def __get_language(self):
		from utils import get_language
		return get_language(self.__uri)

	def __get_mimetype(self):
		if not self.__uri: return None
		from gnomevfs import get_mime_type
		return get_mime_type(self.__uri)

	def __get_session_bus(self):
		from info import session_bus
		return session_bus

	def __get_dbus_iface(self):
		from info import dbus_iface
		return dbus_iface

	def __get_home_folder(self):
		from info import home_folder
		return home_folder

	def __get_desktop_folder(self):
		from info import desktop_folder
		return desktop_folder

	def __get_metadata_folder(self):
		from info import metadata_folder
		return metadata_folder

	def __get_home_plugin_folder(self):
		from info import home_plugin_folder
		return home_plugin_folder

	def __get_core_plugin_folder(self):
		from info import core_plugin_folder
		return core_plugin_folder

	def __get_home_language_plugin_folder(self):
		from info import home_language_plugin_folder
		return home_language_plugin_folder

	def __get_core_language_plugin_folder(self):
		from info import core_language_plugin_folder
		return core_language_plugin_folder

	def __get_scribes_prefix(self):
		from info import scribes_prefix
		return scribes_prefix

	def __get_scribes_executable_path(self):
		from info import scribes_executable_path
		return scribes_executable_path

	def __get_scribes_data_path(self):
		from info import scribes_data_path
		return scribes_data_path

	def __get_scribes_sysconfdir(self):
		from info import scribes_sysconfdir
		return scribes_sysconfdir

	def __get_scribes_data_folder(self):
		from info import scribes_data_folder
		return scribes_data_folder

	def __get_python_path(self):
		from info import python_path
		return python_path

	def __get_version(self):
		from info import version
		return version

	def __get_author(self):
		from info import author
		return author

	def __get_cursor_iterator(self):
		from cursor import get_cursor_iterator
		return get_cursor_iterator(self.__textbuffer)

	def __get_documenters(self):
		from info import documenters
		return documenters

	def __get_artists(self):
		from info import artists
		return artists

	def __get_website(self):
		from info import website
		return website

	def __get_translators(self):
		from info import translators
		return translators

	def __get_copyrights(self):
		from info import copyrights
		return copyrights

	def __get_license(self):
		from license import license_string
		return license_string

	def __get_language_manager(self):
		from gtksourceview2 import language_manager_get_default
		return language_manager_get_default()

	def __get_language_ids(self):
		return self.language_manager.get_language_ids()

	def __get_language_objects(self):
		get_lang_object = lambda x: self.language_manager.get_language(x)
		return map(get_lang_object, self.language_ids)

########################################################################
#
#					Public API Properties
#
########################################################################

	# GUI Widgets
	window = property(__get_window)
	toolbar = property(__get_toolbar)
	textview = property(__get_textview)
	textbuffer = property(__get_textbuffer)
	maincontainer = property(__get_maincontainer)
	toolbarcontainer = property(__get_toolbarcontainer)
	viewcontainer = property(__get_viewcontainer)
	statuscontainer = property(__get_statuscontainer)
	status_image = property(__get_status_image)
	status_image_frame = property(__get_status_image_frame)
	statusone = property(__get_statusone)
	# Global Dialogs
	error_dialog = property(__get_error_dialog, doc="Error dialog for the text editor.")
	message_dialog = property(__get_message_dialog, doc="Message dialog for the text editor.")
	# Global Tipe object
	tip = property(__get_tooltip, doc="Tooltip object for the text editor.")

	# Toolbar Menus
	preference_menu = property(__get_preference_menu, doc="Preference menu for the toolbar.")
	recent_manager = property(__get_recent_manager, doc="Recent manager for the text editor.")
	recent_menu = property(__get_recent_menu, doc="Recent menu for the toolbar.")

	# Global Store object.
	store = property(__get_store, doc="Global storage repository")
	instance_manager=property(__get_instance_manager, doc="Instance manager for the text editor.")
	trigger_manager = triggermanager = property(__get_trigger_manager)
	feedback = property(__get_feedback)
	uri = property(__get_uri)
	encoding = property(__get_encoding)
	encoding_list = property(__get_encoding_list)
	encoding_guess_list = property(__get_encoding_guess_list)
	file_is_saved = property(__get_file_is_saved)
	readonly = is_readonly = property(__get_is_readonly)
	contains_document = property(__get_contains_document)
	gconf_client = property(__get_gconf_client)
	response = property(__get_response)
	can_load_file = property(__get_can_load_file)
	id = property(__get_id)
	language = property(__get_language)
	mimetype = property(__get_mimetype)
	will_load_document = property(__get_will_load_documents)
	session_bus = property(__get_session_bus)
	home_folder = property(__get_home_folder)
	desktop_folder = property(__get_desktop_folder)
	home_plugin_folder = property(__get_home_plugin_folder)
	core_plugin_folder = property(__get_core_plugin_folder)
	home_language_plugin_folder = property(__get_home_language_plugin_folder)
	core_language_plugin_folder = property(__get_core_language_plugin_folder)
	dbus_iface = property(__get_dbus_iface)
	metadata_folder = property(__get_metadata_folder)
	scribes_prefix = property(__get_scribes_prefix)
	scribes_executable_path = property(__get_scribes_executable_path)
	scribes_sysconfdir = property(__get_scribes_sysconfdir)
	scribes_data_path = property(__get_scribes_data_path)
	scribes_data_folder = property(__get_scribes_data_folder)
	python_path = property(__get_python_path)
	version = property(__get_version)
	author = property(__get_author)
	documenters = property(__get_documenters)
	artists = property(__get_artists)
	website = property(__get_website)
	translators = property(__get_translators)
	copyrights = property(__get_copyrights)
	license = property(__get_license)
	cursor = cursor_position = cursor_iterator = property(__get_cursor_iterator)
	language_manager = property(__get_language_manager)
	language_ids = property(__get_language_ids)
	language_objects = property(__get_language_objects)

########################################################################
#
#						Public API Methods
#
########################################################################

	def load_uri(self, uri, encoding="utf-8"):
		self.__can_load_file = False
		from FileLoader import FileLoader
		FileLoader(self, uri, encoding)
		return False

	def create_new_file(self):
		from info import desktop_folder
		from os.path import exists
		if exists(desktop_folder):
			# Save to the desktop folder if it exists.
			folder = desktop_folder
		else:
			# Save to the home folder if the desktop folder does not exists.
			from info import home_folder
			folder = home_folder
		# A count to append to unsaved documents if many unsaved documents
		# exists in folder.
		count = 1
		from internationalization import msg0025
		from dircache import listdir
		file_list = listdir(folder)
		# Calculate count to append to unsaved documents.
		while True:
			newfile = msg0025 + " " + str(count)
			if newfile in file_list:
				count += 1
			else:
				break
		newfile = folder + "/" + newfile
		from gnomevfs import make_uri_from_shell_arg
		self.__uri = make_uri_from_shell_arg(newfile)
		return

	def get_encoding_manager(self):
		return self.__encoding_manager

	def register_termination_id(self):
		"""
		Register a unique identification with the text editor.

		Objects that need to perform special operations before the text editor
		quits, need to call this method when they are initially created. This
		function generates a unique identification number for objects. The
		identification number should be used as an argument to the
		unregister_termination_id method after the object has finished performing
		its special operation, so that the text editor can quit successfully.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.

		@return: A unique identification number.
		@rtype: A Float object.
		"""
		from utils import generate_random_number
		termination_id = generate_random_number(self.__termination_queue)
		self.__termination_queue.add(termination_id)
		return termination_id

	def unregister_termination_id(self, termination_id):
		"""
		Remove unique identification number from the text editor's termination
		registration queue.

		This function disassociates an object from the text editor so that the
		editor can proceed to quit successfully.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.

		@param termination_id: A unique identification number
		@type termination_id: A Float object.
		"""
		if termination_id in self.__termination_queue:
			self.__termination_queue.remove(termination_id)
		if not self.__termination_queue:
			from gobject import timeout_add
			timeout_add(100, self.__destroy)
		return

	def block_response(self):
		return self.__instance_manager.block_response()

	def unblock_response(self):
		return self.__instance_manager.unblock_response()

	def register_object(self):
		return self.register_termination_id()

	def unregister_object(self, object_id):
		return self.unregister_termination_id(object_id)

	def trigger(self, string):
		self.__trigger_manager.trigger(string)
		return

	def create_trigger(self, name, accelerator=None, description=None, error=True, removable=True):
		from Trigger import Trigger
		trigger = Trigger(name, accelerator, description, error, removable)
		return trigger

	def add_trigger(self, trigger):
		self.__trigger_manager.add_trigger(trigger)
		return

	def add_triggers(self, triggers):
		self.__trigger_manager.add_triggers(triggers)
		return

	def remove_trigger(self, trigger):
		self.__trigger_manager.remove_trigger(trigger)
		return

	def remove_triggers(self, triggers):
		self.__trigger_manager.remove_triggers(triggers)
		return

	def show_error_message(self, message, title=None, window=None):
		self.__error_dialog.show_message(message, title, window)
		return

	def show_message(self, message, title=None, window=None):
		self.__message_dialog.show_message(message, title, window)
		return

	def add_object(self, name, instance):
		store_id =	self.__store.add_object(name, instance)
		return store_id

	def remove_object(self, name, store_id):
		self.__store.remove_object(name, store_id)
		return

	def add_global_object(self, name, instance):
		return self.__instance_manager.add_object(name, instance)

	def remove_global_object(self, name, object_id):
		return self.__instance_manager.remove_object(name, object_id)

	def get_global_object(self, name):
		return self.__instance_manager.get_object(name)

	def get_save_processor(self):
		return self.__instance_manager.get_save_processor()

	def show_busy_cursor(self):
		from cursor import show_busy_textview_cursor
		return show_busy_textview_cursor(self.__textview)

	def show_normal_cursor(self):
		from cursor import show_textview_cursor
		return show_textview_cursor(self.__textview)

	def get_word_before_cursor(self):
		from cursor import get_word_before_cursor
		return get_word_before_cursor(self.__textbuffer)

	def can_read_write(self):
		from utils import check_uri_permission
		return check_uri_permission(self.uri)

	def find_file(self, file_path):
		from utils import find_file
		return find_file(file_path)

	def get_object(self, name):
		return self.__store.get_object(name)

	def open_files(self, uris, encoding="utf-8"):
		return self.__instance_manager.open_files(uris, encoding)

	def close_files(self, uris):
		return self.__instance_manager.close_files(uris)

	def focus_file(self, uri):
		return self.__instance_manager.focus_file(uri)

	def get_uris(self):
		return self.__instance_manager.get_uris()

	def get_text(self):
		begin, end = self.__textbuffer.get_bounds()
		return self.__textbuffer.get_text(begin, end)

	def set_tip(self, instance, tip):
		self.__tip.set_tip(instance, tip)
		return

	def create_scrollwin(self):
		from utils import create_scrollwin
		return create_scrollwin()

	def convert_color_to_string(self, color):
		from utils import convert_color_to_spec
		return convert_color_to_spec(color)

	def convert_color_to_spec(self, style):
		return self.convert_color_to_string(style)

	def get_cursor_position(self):
		from cursor import get_cursor_iterator
		return get_cursor_iterator(self.__textbuffer)

	def create_button_box(self, stock_id, string):
		from utils import create_button_box
		return create_button_box(stock_id, string)

	def create_button(self, stock_id, string):
		from utils import create_button
		return create_button(stock_id, string)

	def get_cursor_iterator(self):
		return self.get_cursor_position()

	def get_cursor_line(self):
		from cursor import get_cursor_line
		return get_cursor_line(self.__textbuffer)

	def move_view_to_cursor(self):
		from cursor import move_view_to_cursor
		return move_view_to_cursor(self.__textview)

	def word_to_cursor(self):
		from cursor import word_to_cursor
		return word_to_cursor(self.__textbuffer)

	def get_cursor_window_coordinates(self):
		from cursor import get_cursor_window_coordinates
		return get_cursor_window_coordinates(self.__textview)

	def get_cursor_size(self):
		from cursor import get_cursor_size
		return get_cursor_size(self.__textview)

	def select_row(self, treeview):
		from utils import select_row
		return select_row(treeview)

	def create_image(self, image_file):
		from utils import create_image
		return create_image(image_file)

	def generate_random_number(self, sequence):
		from utils import generate_random_number
		return generate_random_number(sequence)

	def mark(self, iterator, alignment="right"):
		if alignment == "right":
			mark = self.__textbuffer.create_mark(None, iterator, False)
		else:
			mark = self.__textbuffer.create_mark(None, iterator, True)
		return mark

	def delete_mark(self, mark):
		if mark.get_deleted(): return
		self.__textbuffer.delete_mark(mark)
		return

	def init_authentication_manager(self):
		self.__instance_manager.init_authentication_manager()
		return

	def get_editor_instances(self):
		return self.__instance_manager.get_editor_instances()

	def center_current_line(self):
		from cursor import move_view_to_cursor
		move_view_to_cursor(self.__textview)
		return

	def disconnect_signal(self, signal_id, object_ref):
		from utils import disconnect_signal
		disconnect_signal(signal_id, object_ref)
		return

	def delete_attributes(self, object_ref):
		#from utils import delete_attributes
		#delete_attributes(object_ref)
		return

	def create_menuitem(self, string, stock_id=None):
		from utils import create_menuitem
		return create_menuitem(string, stock_id)

	def calculate_resolution_independence(self, window, width, height):
		from utils import calculate_resolution_independence
		return calculate_resolution_independence(window, width, height)

	def update_status_message(self, message=None, icon=None, time=7):
		return self.__feedback.update_status_message(message, icon, time)

	def set_message(self, message=None, icon=None):
		message_id = self.__feedback.set_modal_message(message, icon)
		return message_id

	def unset_message(self, message_id, reset=True):
		self.__feedback.unset_modal_message(message_id, reset)
		return

	def start_spinner(self):
		self.__feedback.start_spinner()
		return

	def stop_spinner(self):
		self.__feedback.stop_spinner()
		return

	def show_encoding_error(self, title, uri):
		self.__encoding_error_dialog.show_message(title, uri)
		return

	def forward_to_line_end(self, iterator):
		if iterator.ends_line(): return iterator
		iterator.forward_to_line_end()
		return iterator

	def backward_to_line_begin(self, iterator):
		if iterator.starts_line(): return iterator
		while True:
			iterator.backward_char()
			if iterator.starts_line(): break
		return iterator

	def get_line_text(self, iterator):
		begin = self.backward_to_line_begin(iterator.copy())
		end = self.forward_to_line_end(iterator.copy())
		text = self.__textbuffer.get_text(begin, end)
		return text

	def is_empty_line(self, iterator):
		text = self.get_line_text(iterator).strip(" \t\n\x0D\x0A")
		if text: return False
		return True

########################################################################

	def __create_widgets(self):
		"""
		Create visible graphic user interface components.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.
		"""
		from Window import ScribesWindow
		self.__window = ScribesWindow(self)
		from MainContainer import ScribesMainContainer
		self.__maincontainer = ScribesMainContainer(self)
		from ToolbarContainer import ScribesToolbarContainer
		self.__toolbarcontainer = ScribesToolbarContainer(self)
		from ViewContainer import ScribesViewContainer
		self.__viewcontainer = ScribesViewContainer(self)
		from StatusContainer import ScribesStatusContainer
		self.__statuscontainer = ScribesStatusContainer(self)
		# Create the text editor's buffer.
		from TextBuffer import ScribesTextBuffer
		self.__textbuffer = ScribesTextBuffer(self)
		self.emit("buffer-created")
		# Create the text editor's view. The view is a container for the
		# text editor's buffer.
		from TextView import ScribesTextView
		self.__textview = ScribesTextView(self)
		# Create the text editor's toolbar.
		from Toolbar import ScribesToolbar
		self.__toolbar = ScribesToolbar(self)
		# Create statusbar image.
		from gtk import Image
		self.__status_image	 = Image()
		# A container to hold the statusbar image.
		from gtk import Frame
		self.__status_image_frame = Frame()
		# Create the text editor's statusbars.
		from StatusBar import StatusOne, StatusTwo, StatusThree
		self.__statusone  = StatusOne(self)
		self.__statustwo = StatusTwo(self)
		self.__statusthree = StatusThree(self)
		self.emit("created-widgets")
		return False

	def __arrange_widgets(self):
		"""
		Arrange text editor widgets then display it.

		After the text editor graphic user interface components are created,
		this function arranges the widgets by packing them into the editor's
		main containers. After which, the text editor is displayed. This
		function is called repeatedly unless its return value is False.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.
		"""
		self.__maincontainer.pack_start(self.__toolbarcontainer, False, False, 0)
		self.__maincontainer.pack_start(self.__viewcontainer, True, True, 1)
		self.__maincontainer.pack_start(self.__statuscontainer, False, False, 0)
		# Scroll window for the text editor.
		from utils import create_scrollwin
		scrollwin = create_scrollwin()
		scrollwin.add(self.__textview)

		# Frame that holds the statusbar image.
		from gtk import SHADOW_IN
		self.__status_image_frame.set_shadow_type(SHADOW_IN)
		self.__status_image_frame.add(self.status_image)
		self.__status_image.clear()
		self.__status_image.hide_all()
		self.__status_image_frame.hide_all()

		# Pack widgets into the editor's containers.
		self.__toolbarcontainer.pack_start(self.__toolbar, True, True, 0)
		self.__viewcontainer.pack_start(scrollwin, True, True, 0)
		self.__statuscontainer.pack_start(self.__status_image_frame, False, False,0)
		self.__statuscontainer.pack_start(self.__statusone, True, True, 0)
		self.__statuscontainer.pack_start(self.__statustwo, False, True, 0)
		self.__statuscontainer.pack_start(self.__statusthree, False, True, 0)
		self.__maincontainer.resize_children()
		self.emit("gui-created")
		return False

	def __destroy(self):
		self.__textview.destroy()
		self.__status_image.destroy()
		self.__status_image_frame.destroy()
		self.__statuscontainer.destroy()
		self.__window.destroy()
		from utils import disconnect_signal
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self)
		disconnect_signal(self.__signal_id_3, self)
		disconnect_signal(self.__signal_id_4, self)
		disconnect_signal(self.__signal_id_5, self)
		disconnect_signal(self.__signal_id_6, self)
		disconnect_signal(self.__signal_id_7, self)
		disconnect_signal(self.__signal_id_8, self)
		disconnect_signal(self.__signal_id_9, self)
		disconnect_signal(self.__signal_id_10, self)
		disconnect_signal(self.__signal_id_11, self)
		disconnect_signal(self.__signal_id_12, self)
		disconnect_signal(self.__signal_id_13, self)
		disconnect_signal(self.__signal_id_14, self)
		self.__instance_manager.unregister_editor(self, self.__manager_registration_id)
		del self
		self = None
		from gc import collect
		collect()
		return False

########################################################################
#
#					Signal and Event Handlers
#
########################################################################

	def __initialized_attributes_cb(self, editor):
		"""
		Handles callback when the "initialized-attributes" signal is emitted.

		@param self: Reference to this editor instance.
		@type self: An Editor object.
		"""
		self.__create_widgets()
		return

	def __created_widgets_cb(self, editor):
		"""
		Handles callback when the "created-widgets" signal is emitted.

		This function arranges the text editor wigdets after they have
		been created, initializes the editor's feedback system and
		GNOME libraries, and loads a file into the editor window if
		one is passed as an argument to the editor.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager_registration_id = self.__instance_manager.register_editor(self)
		self.__start_core_services()
		return

	def __start_core_services(self):
		"""
		Initialize key objects before the GUI is displayed.

		This objects need to be initialized immediately after GUI
		elements are created.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.
		"""
		# Initialize encoding manager.
		from EncodingManager import EncodingManager
		self.__encoding_manager = EncodingManager(self)
		# Initialize file modification monitor
#		from FileModificationMonitor import FileModificationMonitor
#		FileModificationMonitor(self)
		# Initialize the object that saves files.
		# Initialize the feedback manager.
		from Feedback import FeedbackManager
		self.__feedback = FeedbackManager(self)
		# Initialize the trigger manager.
		from TriggerManager import TriggerManager
		self.__trigger_manager = TriggerManager(self)
		from NewFileSaver import FileSaver
		FileSaver(self)
		self.emit("started-core-services")
		return

	def __created_widgets_after_cb(self, editor):
		self.__arrange_widgets()
		return

	def __gui_created_after_cb(self, editor):
		return

	def __started_core_services_cb(self, *args):
		try:
			# Load file if any.
			from gobject import idle_add, PRIORITY_LOW
			if not self.__file_uri: raise ValueError
			idle_add(self.load_uri, self.__file_uri.strip(), self.__encoding)
		except ValueError:
			pass
		finally:
			# Initialize plugins
			idle_add(self.__initialize_plugins, priority=5000)
			idle_add(self.__initialize_language_plugins, priority=5000)
		return False

	def __initialize_plugins(self):
		from PluginManager import PluginManager
		PluginManager(self)
		return False

	def __initialize_language_plugins(self):
		from LanguagePluginManager import PluginManager
		PluginManager(self)
		return False

	def __checking_document_cb(self, editor, uri):
		self.__can_load_file = False
		self.__uri = uri
		return

	def __loaded_document_cb(self, *args):
		self.__can_load_file = False
		self.__contains_document = True
#		print "Language ID: ", self.language.get_id()
		return

	def __loaded_document_after_cb(self, *args):
		self.__can_load_file = False
		self.__contains_document = True
	#	print "Encoding is: ", self.encoding
		return

	def __load_error_cb(self, *args):
		self.__can_load_file = True
		self.__uri = None
		return

	def __saved_document_cb(self, *args):
		self.__file_is_saved = True
		return

	def __renamed_document_cb(self, editor, uri, *args):
		self.__file_is_saved = True
		self.__uri = uri
		self.__can_load_file = False
		self.__contains_document = True
		return

	def __reload_document_cb(self, *args):
		self.__file_is_saved = True
		self.__can_load_file = True
		self.__contains_document = False
		self.load_uri(self.__uri)
		return

	def __rename_document_cb(self, editor, uri, *args):
		self.__uri = uri
		return

	def __enable_readonly_cb(self, *args):
		self.__is_readonly = True
		return

	def __disable_readonly_cb(self, *args):
		self.__is_readonly = False
		return

	def __modified_document_cb(self, *args):
		self.__file_is_saved = False
		self.__contains_document = True
		self.__can_load_file = False
		return False

########################################################################
#
#						Editor Attributes
#
########################################################################

	def __init_attributes(self, manager, file_uri, encoding):
		"""
		Initialize data attributes.

		@param self: Reference to this editor instance.
		@type self: An Editor object.

		@param manager: An object that manages editor instances.
		@type manager: An EditorManager object.

		@param file_uri: A file to open.
		@param type: A String object.
		"""
		# A function to improve responsiveness.
		#from utils import response
		self.__id = id(self)
		self.__encoding = encoding
		# An object that manages instances of editors.
		self.__instance_manager = manager
		self.__response = manager.response
		# A file to open or none.
		self.__file_uri = file_uri
		# Whether or not the editor can load a file.
		self.__can_load_file = True
		self.__encoding_manager = None
		# The text editor quits only after the termination queue is empty. This
		# allows objects that need to perform cleanup or metadata operation
		# to register a unique number in the queue. Registration should occur
		# during the creation of the object. The object is responsible for
		# removing it identification from the queue.
		self.__termination_queue = set([])
		# A storage repository for arbitrary objects.
		from Store import Store
		self.__store = Store(self)
		# Global tooltip object.
		from tooltips import create_tooltips
		self.__tip = create_tooltips()
		# Global error dialog.
		from ErrorDialog import ScribesErrorDialog
		self.__error_dialog = ScribesErrorDialog(self)
		# Global message dialog.
		from MessageDialog import ScribesMessageDialog
		self.__message_dialog = ScribesMessageDialog(self)
		from EncodingErrorWindow import EncodingErrorWindow
		self.__encoding_error_dialog = EncodingErrorWindow(self)
		# Reference to the preference menu on the toolbar.
		from PreferenceMenu import PreferenceMenu
		self.__preference_menu = PreferenceMenu(self)
		# Reference to the recent manager used by the recent menu.
		from RecentManager import RecentManager
		self.__recent_manager = RecentManager(self)()
		# Reference to the recent menu on the toolbar.
		from RecentMenu import RecentMenu
		self.__recent_menu = RecentMenu(self)
		self.__file_is_saved = True
		self.__is_readonly = False
		self.__contains_document = False
		# A unique number given to this editor by the object that manages instances.
		self.__manager_registration_id = None
		# Reference to successfully loaded file.
		self.__uri = None
		# Reference to the feedback manager.
		self.__feedback = None
		# Reference to the trigger manager.
		self.__trigger_manager = None
		# Editor widgets
		self.__window = None
		self.__toolbar = None
		self.__textbuffer = None
		self.__textview = None
		self.__statusone = None
		self.__statustwo = None
		self.__statusthree = None
		self.__status_image_frame = None
		self.__status_image = None
		self.__maincontainer = None
		self.__toolbarcontainer = None
		self.__viewcontainer = None
		self.__statuscontainer = None
		# A signal emitted after crucial data attributes have been created.
		self.emit("initialized-attributes")
		return False

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__get_textbuffer)
			bind(self.__get_textview)
			bind(self.__get_core_plugin_folder)
			bind(self.__get_is_readonly)
			bind(self.__get_uri)
			bind(self.get_cursor_position)
		except ImportError:
			pass
		return False
