from Globals import data_folder, metadata_folder, home_folder, desktop_folder
from Globals import session_bus, core_plugin_folder, home_plugin_folder
from Globals import home_language_plugin_folder, core_language_plugin_folder
from Globals import version, author, documenters, artists, website
from Globals import copyrights, translators, python_path, dbus_iface
from License import license_string
from gnomevfs import URI, get_uri_from_local_path
from DialogFilters import create_filter_list
from gtksourceview2 import language_manager_get_default
from EncodingGuessListMetadata import get_value as get_encoding_guess_list
from EncodedFilesMetadata import get_value as get_encoding
from EncodingMetadata import get_value as get_encoding_list
from Utils import get_language, word_pattern
from SupportedEncodings import get_supported_encodings
from gettext import gettext as _

from SIGNALS import Signals

class Editor(Signals):

	def __init__(self, manager, uri=None, encoding="utf-8"):
		Signals.__init__(self)
		self.set_data("InstanceManager", manager)
		from RegistrationManager import Manager
		Manager(self)
		from ContentDetector import Detector
		Detector(self, uri)
		from FileModificationMonitor import Monitor
		Monitor(self)
		from URIManager import Manager
		Manager(self, uri)
		from LanguageManager import Manager
		Manager(self, uri)
		from SchemeManager import Manager
		Manager(self)
		from GladeObjectManager import Manager
		Manager(self)
		from BusyManager import Manager
		Manager(self)
		# Manages the behavior of the window.
		from Window import Window
		Window(self, uri)
		# Manages he behavior of the buffer's container.
		from TextView import View
		View(self)
		# Manages the behavior of the buffer.
		from TextBuffer import Buffer
		Buffer(self)
		# Manages error and information window.
		from MessageWindow import Window
		Window(self)
		# Manages encoding information.
		from EncodingManager import Manager
		Manager(self)
		# Object responsible for sending data to external process via
		# DBus to save files. An external process does the I/O operations.
		from SaveCommunicator import Communicator
		Communicator(self)
		# Object responsible for saving files.
		from FileSaver import Saver
		Saver(self)
		# Object responsible for deciding when to save files
		# automatically.
		from SaveManager import Manager
		Manager(self)
		# Manages window that shows supported encodings.
		from SupportedEncodingsGUIManager import Manager
		Manager(self)
		# Object responsible for showing encoding error window. The window
		# allows users to load files with the correct encoding.
		from EncodingErrorManager import Manager
		Manager(self)
		# Object that share information for encoding combo box.
		from EncodingComboBoxDataManager import Manager
		Manager(self)
		from StatusFeedback import Feedback
		Feedback(self)
		from StatusImage import Image
		Image(self)
		from StatusCursorPosition import Position
		Position(self)
		from StatusInsertionType import Type
		Type(self)
		from StatusContainer import Container
		Container(self)
		from RecentManager import Manager
		Manager(self)
		# Toolbar object.
		from Toolbar import Toolbar
		Toolbar(self)
		from PopupMenuManager import Manager
		Manager(self)
		from TriggerManager import Manager
		Manager(self)
		from ReadonlyManager import Manager
		Manager(self)
		# Register with instance manager after a successful editor
		# initialization.
		manager.register_editor(self)
		from BarObjectManager import Manager
		Manager(self)
		from FullScreenManager import Manager
		Manager(self)
		# Load files or initialize plugins. Always load files, if any,
		# before initializing plugin systems. This should be the last
		# line in this method.
		from PluginSystemInitializer import Initializer
		Initializer(self, uri)
		from URILoader.Manager import Manager
		Manager(self, uri, encoding)
		from sys import getcheckinterval
		print getcheckinterval()

################################################################
#
#						Public APIs
#
################################################################

	imanager = property(lambda self: self.get_data("InstanceManager"))
	gui = property(lambda self: self.get_data("gui"))
	window = property(lambda self: self.gui.get_widget("Window"))
	textview = property(lambda self: self.gui.get_widget("ScrolledWindow").get_child())
	textbuffer = property(lambda self: self.textview.get_property("buffer"))
	toolbar = property(lambda self: self.gui.get_widget("Toolbar"))
	statusbar = property(lambda self: self.gui.get_widget("StatusContainer"))
	id_ = property(lambda self: id(self))
	uri = property(lambda self: self.get_data("uri"))
	uris = property(lambda self: self.imanager.get_uris())
	# All editor instances
	objects = instances = property(lambda self: self.imanager.get_editor_instances())
	uri_object = property(lambda self: self.get_data("uri_object"))
	name = property(lambda self: self.uri_object.short_name if self.uri else None)
	language_object = property(lambda self: self.get_data("language_object"))
	language = property(lambda self: self.get_data("language"))
	language_manager = property(lambda self: language_manager_get_default())
	language_ids = property(lambda self: self.language_manager.get_language_ids())
	language_objects = property(lambda self: [self.language_manager.get_language(language) for language in self.language_ids])
	style_scheme_manager = property(lambda self: self.get_data("style_scheme_manager"))
	readonly = property(lambda self: self.get_data("readonly"))
	modified = property(lambda self: self.get_data("modified"))
	contains_document = property(lambda self: self.get_data("contains_document"))
	encoding = property(lambda self:get_encoding(self.uri))
	encoding_list = property(lambda self: get_encoding_list())
	encoding_guess_list = property(lambda self: get_encoding_guess_list())
	# textview and textbuffer information
	cursor = property(lambda self: self.textbuffer.get_iter_at_offset(self.textbuffer.get_property("cursor_position")))
	text = property(lambda self: self.textbuffer.get_text(*(self.textbuffer.get_bounds())))
	# Global information
	data_folder = property(lambda self: data_folder)
	metadata_folder = property(lambda self: metadata_folder)
	home_folder = property(lambda self: home_folder)
	desktop_folder = property(lambda self: desktop_folder)
	home_folder_uri = property(lambda self: get_uri_from_local_path(self.home_folder))
	desktop_folder_uri = property(lambda self: get_uri_from_local_path(self.desktop_folder))
	core_plugin_folder = property(lambda self: core_plugin_folder)
	home_plugin_folder = property(lambda self: home_plugin_folder)
	core_language_plugin_folder = property(lambda self: core_language_plugin_folder)
	home_language_plugin_folder = property(lambda self: home_language_plugin_folder)
	session_bus = property(lambda self: session_bus)
	python_path = property(lambda self: python_path)
	dbus_iface = property(lambda self: dbus_iface)
	version = property(lambda self: version)
	copyrights = property(lambda self: copyrights)
	license = property(lambda self: license_string)
	translators = property(lambda self: translators)
	documenters = property(lambda self: documenters)
	artists = property(lambda self: artists)
	author = property(lambda self: author)
	website = property(lambda self: website)
	save_processor = property(lambda self: self.imanager.get_save_processor())
	supported_encodings = property(lambda self: get_supported_encodings())
	word_pattern = property(lambda self: word_pattern)
	selection_range = property(lambda self: self.get_selection_range())
	selection_bounds = property(lambda self: self.textbuffer.get_selection_bounds())
	selected_text = property(lambda self: self.textbuffer.get_text(*(self.selection_bounds)))
	has_selection = property(lambda self: self.textbuffer.props.has_selection)
	pwd = property(lambda self: str(URI(self.uri).parent.path) if self.uri else self.desktop_folder)
	pwd_uri = property(lambda self: str(URI(self.uri).parent) if self.uri else get_uri_from_local_path(self.desktop_folder))
	dialog_filters = property(lambda self: create_filter_list())
	recent_manager = property(lambda self: self.get_data("RecentManager"))
	bar_is_active = property(lambda self: self.get_data("bar_is_active"))

	def optimize(self, functions):
		try:
			self.response()
			from psyco import bind
			[bind(function) for function in functions]
			self.response()
		except ImportError:
			pass
		return False

	def help(self):
		from gnome import help_display
		success = True if help_display("/scribes.xml") else False
		message = _("Launching user guide") if success else _("Failed to launch user guide")
		show = self.update_message
		show(message, "help", 10) if success else show(message, "fail", 7)
		return

	def new(self):
		self.response()
		return self.imanager.open_files()

	def shutdown(self):
		self.response()
		self.close()
		self.response()
		return self.imanager.close_all_windows()

	def close(self, save_first=True):
		self.response()
		self.emit("close", save_first)
		self.response()
		return False

	def fullscreen(self, value=True):
		self.emit("fullscreen", value)
		return

	def toggle_fullscreen(self):
		self.emit("toggle-fullscreen")
		return False

	def toggle_readonly(self):
		self.emit("toggle-readonly")
		return False

	def refresh(self, grab_focus=True):
		self.emit("refresh", grab_focus)
		return False

	def save_file(self, uri, encoding="utf-8"):
		self.response()
		self.emit("save-file", uri, encoding)
		self.response()
		return

	def rename_file(self, uri, encoding="utf-8"):
		self.emit("rename-file", uri, encoding)
		return

	def load_file(self, uri, encoding, readonly=False):
		self.response()
		self.emit("load-file", uri, encoding)
		self.response()
		return False

	def open_file(self, uri, encoding="utf8"):
		self.response()
		self.imanager.open_files([uri], encoding)
		self.response()
		return

	def open_files(self, uris, encoding="utf8"):
		self.response()
		self.imanager.open_files(uris, encoding)
		self.response()
		return

	def focus_file(self, uri):
		self.response()
		self.imanager.focus_file(uri)
		self.response()
		return

	def focus_by_id(self, id_):
		self.response()
		self.imanager.focus_by_id(id_)
		self.response()
		return

	def close_file(self, uri):
		self.response()
		self.imanager.close_files([uri])
		self.response()
		return

	def close_files(self, uris):
		self.response()
		self.imanager.close_files(uris)
		self.response()
		return

	def create_uri(self, uri, exclusive=True):
		from Utils import create_uri
		return create_uri(uri, exclusive)

	def create_image(self, path):
		from Utils import create_image
		return create_image(path)

	def register_object(self, instance):
		self.emit("register-object", instance)
		return False

	def unregister_object(self, instance):
		self.emit("unregister-object", instance)
		return False

	def calculate_resolution_independence(self, window, width, height):
		from Utils import calculate_resolution_independence
		return calculate_resolution_independence(window, width, height)

	def disconnect_signal(self, sigid, instance):
		from Utils import disconnect_signal
		return disconnect_signal(sigid, instance)

	def move_view_to_cursor(self, align=False, iterator=None):
		if iterator is None: iterator = self.cursor
		self.textview.scroll_to_iter(iterator, 0.001, use_align=align, xalign=1.0)
		return False

	def response(self):
		return self.imanager.response()

	def busy(self, busy=True):
		self.emit("private-busy", busy)
		return False

	def show_load_encoding_error_window(self):
		self.emit("private-encoding-load-error")
		return False

	def show_supported_encodings_window(self, window=None):
		window = window if window else self.window
		self.emit("supported-encodings-window", window)
		return

	def show_error(self, title, message, window=None, busy=False):
		window = window if window else self.window
		self.emit("show-error", title, message, window, busy)
		return False

	def show_info(self, title, message, window=None, busy=False):
		window = window if window else self.window
		self.emit("show-info", title, message, window, busy)
		return False

	def emit_combobox_encodings(self):
		self.emit("combobox-encoding-data?")
		return False

	def spin_throbber(self, spin=True):
		self.emit("spin-throbber", spin)
		return False

	def update_message(self, message, icon_name="scribes", time=5):
		self.emit("update-message", message, icon_name, time)
		return False

	def set_message(self, message, icon_name="scribes"):
		self.emit("set-message", message, icon_name)
		return False

	def unset_message(self, message, icon_name="scribes"):
		self.emit("unset-message", message, icon_name)
		return False

	def get_toolbutton(self, name):
		toolbutton = None
		for toolbutton in self.toolbar.get_children():
			if name != toolbutton.get_property("name"): continue
			toolbutton = toolbutton
			break
		return toolbutton

	def get_indentation(self, iterator=None):
		if iterator is None: iterator = self.cursor.copy()
		start = self.backward_to_line_begin(iterator.copy())
		if start.is_end() or start.ends_line(): return ""
		end = start.copy()
		while end.get_char() in (" ", "\t"): end.forward_char()
		return self.textbuffer.get_text(start, end)

	def redo(self):
		self.emit("redo")
		return

	def undo(self):
		self.emit("undo")
		return

	def backward_to_line_begin(self, iterator=None):
		if iterator is None: iterator = self.cursor
		from Utils import backward_to_line_begin
		return backward_to_line_begin(iterator.copy())

	def forward_to_line_end(self, iterator=None):
		if iterator is None: iterator = self.cursor
		from Utils import forward_to_line_end
		return forward_to_line_end(iterator.copy())

	def create_trigger(self, name, accelerator=None, description=None, error=True, removable=True):
		from Trigger import Trigger
		trigger = Trigger(self, name, accelerator, description, error, removable)
		return trigger

	def trigger(self, name):
		self.emit("trigger", name)
		return False

	def add_trigger(self, trigger):
		self.emit("add-trigger", trigger)
		return False

	def remove_trigger(self, trigger):
		self.emit("remove-trigger", trigger)
		return False

	def add_triggers(self, triggers):
		self.emit("add-triggers", triggers)
		return False

	def remove_triggers(self, triggers):
		self.emit("remove-triggers", triggers)
		return False

	def select_row(self, treeview):
		from Utils import select_row
		return select_row(treeview)

	def mark(self, iterator, alignment="right"):
		value = False if alignment == "right" else True
		mark = self.textbuffer.create_mark(None, iterator, value)
		return mark

	def create_left_mark(self, iterator=None):
		if iterator: return self.mark(iterator, "left")
		return self.mark(self.cursor, "left")

	def create_right_mark(self, iterator=None):
		if iterator: return self.mark(iterator, "right")
		return self.mark(self.cursor, "right")

	def delete_mark(self, mark):
		if mark.get_deleted(): return
		self.textbuffer.delete_mark(mark)
		return

	def inside_word(self, iterator=None, pattern=None):
		if iterator is None: iterator = self.cursor
		if pattern is None: pattern = self.word_pattern
		from Word import inside_word
		return inside_word(iterator, pattern)

	def is_empty_line(self, iterator=None):
		if iterator is None: iterator = self.cursor
		start = self.backward_to_line_begin(iterator)
		if start.ends_line(): return True
		end = self.forward_to_line_end(iterator)
		text = self.textbuffer.get_text(start, end).strip(" \t\n\r")
		if text: return False
		return True

	def get_line_bounds(self, iterator=None):
		if iterator is None: iterator = self.cursor
		start = self.backward_to_line_begin(iterator)
		end = self.forward_to_line_end(iterator)
		return start, end

	def get_line_text(self, iterator=None):
		if iterator is None: iterator = self.cursor
		return self.textbuffer.get_text(*(self.get_line_bounds(iterator)))

	def get_word_boundary(self, iterator=None, pattern=None):
		if iterator is None: iterator = self.cursor
		if pattern is None: pattern = self.word_pattern
		from Word import get_word_boundary
		return get_word_boundary(iterator, pattern)

	def find_matching_bracket(self, iterator=None):
		if iterator is None: iterator = self.cursor
		from Utils import find_matching_bracket
		return find_matching_bracket(iterator)

	def get_current_folder(self, globals_):
		from os.path import split
		folder = split(globals_["__file__"])[0]
		return folder

	def uri_is_folder(self, uri):
		from Utils import uri_is_folder
		return uri_is_folder(uri)

	def add_bar_object(self, bar):
		self.emit("add-bar-object", bar)
		return

	def remove_bar_object(self, bar):
		self.emit("remove-bar-object", bar)
		return

	def add_shortcut(self, shortcut):
		return self.imanager.add_shortcut(shortcut)

	def remove_shortcut(self, shortcut):
		return self.imanager.remove_shortcut(shortcut)

	def get_shortcuts(self):
		return self.imanager.get_shortcuts()

	def add_to_popup(self, menuitem):
		self.emit("add-to-popup", menuitem)
		return False

	def add_to_pref_menu(self, menuitem):
		self.emit("add-to-pref-menu", menuitem)
		return False

	def remove_from_pref_menu(self, menuitem):
		self.emit("remove-from-pref-menu", menuitem)
		return False

	def create_menuitem(self, name, stock=None):
		from Utils import create_menuitem
		return create_menuitem(name, stock)

	def get_glade_object(self, globals_, basepath, object_name):
		from os.path import join
		folder = self.get_current_folder(globals_)
		file_ = join(folder, basepath)
		from gtk.glade import XML
		glade = XML(file_, object_name, "scribes")
		return glade

	def set_vm_interval(self, response=True):
		#FIXME: This function is deprecated!
		return

	def get_selection_range(self):
		if self.textbuffer.props.has_selection is False: return 0
		start, end = self.textbuffer.get_selection_bounds()
		return (end.get_line() - start.get_line()) + 1
