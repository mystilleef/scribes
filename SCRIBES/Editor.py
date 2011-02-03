import EditorImports
from SIGNALS import Signals

class Editor(Signals):

	def __init__(self, manager, uri=None, encoding="utf-8", stdin=None):
		Signals.__init__(self)
		from ServicesInitializer import Initializer
		Initializer(self, manager, uri, encoding, stdin)
		self.__count = 0

########################################################################
#
#						Public APIs
#
########################################################################

	@property
	def window_is_active(self):
		from Utils import window_is_active
		return window_is_active(self)

	@property
	def id_(self): return id(self)

	@property
	def spaces_instead_of_tabs(self): return self.view.get_insert_spaces_instead_of_tabs()

	@property
	def tabs_instead_of_spaces(self): return not self.view.get_insert_spaces_instead_of_tabs()

	@property
	def tab_width(self): return self.view.get_tab_width()

	@property
	def indentation_width(self): return self.view.get_tab_width()

	@property
	def line_text(self): return self.get_line_text()

	imanager = property(lambda self: self.get_data("InstanceManager"))
	gui = property(lambda self: self.get_data("gui"))
	window = property(lambda self: self.gui.get_widget("Window"))
	textview = view = property(lambda self: self.gui.get_widget("ScrolledWindow").get_child())
	textbuffer = buf = buffer_ = property(lambda self: self.textview.get_property("buffer"))
	toolbar = property(lambda self: self.get_data("Toolbar"))
	uri = property(lambda self: self.get_data("uri"))
	uris = property(lambda self: self.imanager.get_uris())
	# All editor instances
	objects = instances = property(lambda self: self.imanager.get_editor_instances())
	name = property(lambda self: EditorImports.File(self.uri).query_info("*").get_display_name() if self.uri else None)
	triggers = property(lambda self: self.get_data("triggers"))
	filename = property(lambda self: EditorImports.File(self.uri).get_path() if self.uri else "")
	language_object = property(lambda self: self.get_data("language_object"))
	language = property(lambda self: self.get_data("language"))
	language_manager = property(lambda self: EditorImports.language_manager_get_default())
	language_ids = property(lambda self: self.language_manager.get_language_ids())
	language_objects = property(lambda self: [self.language_manager.get_language(language) for language in self.language_ids])
	style_scheme_manager = property(lambda self: self.get_data("style_scheme_manager"))
	readonly = property(lambda self: self.get_data("readonly"))
	modified = property(lambda self: self.get_data("modified"))
	contains_document = property(lambda self: self.get_data("contains_document"))
	encoding = property(lambda self: EditorImports.get_encoding(self.uri))
	encoding_list = property(lambda self: EditorImports.get_encoding_list())
	encoding_guess_list = property(lambda self: EditorImports.get_encoding_guess_list())
	# textview and textbuffer information
	cursor = property(lambda self: self.textbuffer.get_iter_at_offset(self.textbuffer.get_property("cursor_position")))
	text = property(lambda self: self.textbuffer.get_text(*(self.textbuffer.get_bounds())))
	# Global information
	print_settings_filename = property(lambda self: EditorImports.print_settings_filename)
	data_folder = property(lambda self: EditorImports.data_folder)
	metadata_folder = property(lambda self: EditorImports.metadata_folder)
	storage_folder = property(lambda self: EditorImports.storage_folder)
	home_folder = property(lambda self: EditorImports.home_folder)
	desktop_folder = property(lambda self: EditorImports.desktop_folder)
	home_folder_uri = property(lambda self: EditorImports.File(self.home_folder).get_uri())
	desktop_folder_uri = property(lambda self: EditorImports.File(self.desktop_folder).get_uri())
	core_plugin_folder = property(lambda self: EditorImports.core_plugin_folder)
	home_plugin_folder = property(lambda self: EditorImports.home_plugin_folder)
	core_language_plugin_folder = property(lambda self: EditorImports.core_language_plugin_folder)
	home_language_plugin_folder = property(lambda self: EditorImports.home_language_plugin_folder)
	session_bus = property(lambda self: EditorImports.session_bus)
	python_path = property(lambda self: EditorImports.python_path)
	dbus_iface = property(lambda self: EditorImports.dbus_iface)
	version = property(lambda self: EditorImports.version)
	copyrights = property(lambda self: EditorImports.copyrights)
	license = property(lambda self: EditorImports.license_string)
	translators = property(lambda self: EditorImports.translators)
	documenters = property(lambda self: EditorImports.documenters)
	artists = property(lambda self: EditorImports.artists)
	author = property(lambda self: EditorImports.author)
	scribes_theme_folder = property(lambda self: EditorImports.scribes_theme_folder)
	default_home_theme_folder = property(lambda self: EditorImports.default_home_theme_folder)
	website = property(lambda self: EditorImports.website)
	save_processor = property(lambda self: self.imanager.get_save_processor())
	supported_encodings = property(lambda self: EditorImports.supported_encodings)
	word_pattern = property(lambda self: EditorImports.WORD_PATTERN)
	selection_range = property(lambda self: self.get_selection_range())
	selection_bounds = property(lambda self: self.textbuffer.get_selection_bounds())
	newline_character = property(lambda self: self.get_newline_character())
	line_indentation = property(lambda self: self.get_line_indentation())
	selected_text = property(lambda self: self.textbuffer.get_text(*(self.selection_bounds)))
	has_selection = property(lambda self: self.textbuffer.props.has_selection)
	pwd = property(lambda self: EditorImports.File(self.uri).get_parent().get_path() if self.uri else self.desktop_folder)
	pwd_uri = property(lambda self: EditorImports.File(self.uri).get_parent().get_uri() if self.uri else EditorImports.File(self.desktop_folder).get_uri())
	dialog_filters = property(lambda self: EditorImports.create_filter_list())
	bar_is_active = property(lambda self: self.get_data("bar_is_active"))
	completion_window_is_visible = property(lambda self: self.get_data("completion_window_is_visible"))
	minimized = property(lambda self: self.get_data("minimized"))
	maximized = property(lambda self: self.get_data("maximized"))
	in_fullscreen_mode = property(lambda self: self.get_data("in_fullscreen_mode"))
	uniquestamp = property(lambda self: self.get_data("uniquestamp"))
	generate_filename = property(lambda self: self.get_data("generate_filename"))
	mimetype = property(lambda self: self.get_mimetype(self.uri))
	fileinfo = property(lambda self: self.get_fileinfo(self.uri))
	view_bg_color = property(lambda self: self.textview.get_modifier_style().base[-1])
	recent_manager = property(lambda self: self.get_data("RecentManager"))
	last_session_uris = property(lambda self: self.imanager.get_last_session_uris())

	def optimize(self, functions):
		try:
			from psyco import bind
			for function in functions:
				bind(function)
		except ImportError:
			pass
		return False

	def help(self):
		uri = "ghelp:scribes"
		from gtk import show_uri, get_current_event_time
		result = show_uri(self.window.get_screen(), uri, get_current_event_time())
		from gettext import gettext as i18n
		message = i18n("Launching user guide") if result else i18n("Failed to launch user guide")
		image = "help" if result else "fail"
		self.update_message(message, image, 10)
		return

	def new(self, text=None):
		return self.imanager.open_files(stdin=text)

	def shutdown(self):
		self.close()
		return self.imanager.close_all_windows()

	def close(self, save_first=True):
		try:
			if save_first and self.generate_filename: raise ValueError
		except ValueError:
			# Don't save document if buffer contains only whitespaces.
			from string import whitespace
			document_is_empty = False if self.text.strip(whitespace) else True
			save_first = False if document_is_empty else True
		finally:
			self.emit("close", save_first)
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

	def refresh(self, grab_focus=False):
		self.emit("refresh", grab_focus)
		return False

	def reset_text(self, text):
		self.freeze()
		self.buffer_.set_text(text)
		iterator = self.buffer_.get_start_iter()
		self.buffer_.place_cursor(iterator)
		self.thaw()
		return False

	def set_text(self, text):
		self.emit("reset-buffer", "begin")
		self.textbuffer.set_text(text)
		self.emit("reset-buffer", "end")
		return False

	def save_file(self, uri, encoding="utf-8"):
		self.emit("save-file", uri, encoding)
		return

	def rename_file(self, uri, encoding="utf-8"):
		self.emit("rename-file", uri, encoding)
		return

	def load_file(self, uri, encoding="utf-8"):
		self.set_data("contains_document", True)
		self.emit("load-file", uri, encoding)
		return False

	def load_last_session(self):
		uris = self.last_session_uris
		if not uris: return
		self.open_files(uris)
		return

	def open_file(self, uri, encoding="utf8"):
		self.imanager.open_files((uri,), encoding)
		return False

	def open_files(self, uris, encoding="utf8"):
		self.imanager.open_files(tuple(uris), encoding)
		return False

	def focus_file(self, uri):
		self.imanager.focus_file(uri)
		return

	def focus_by_id(self, id_):
		self.imanager.focus_by_id(id_)
		return

	def close_file(self, uri):
		self.imanager.close_files([uri])
		return

	def close_files(self, uris):
		self.imanager.close_files(uris)
		return

	def create_uri(self, uri, exclusive=True):
		from Utils import create_uri
		return create_uri(uri, exclusive)

	def remove_uri(self, uri):
		from Utils import remove_uri
		return remove_uri(uri)

	def create_image(self, path):
		from Utils import create_image
		return create_image(path)

	def freeze(self):
		self.emit("freeze")
		return False

	def thaw(self):
		self.emit("thaw")
		return False

	def register_object(self, instance):
		self.emit("register-object", instance)
		return False

	def show_full_view(self):
		self.emit("show-full-view")
		return False

	def hide_full_view(self):
		self.emit("hide-full-view")
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

	def disconnect_signals(self, data):
		return [self.disconnect_signal(sigid, instance) for sigid, instance in data]

	def move_view_to_cursor(self, align=False, iterator=None):
		if iterator is None: iterator = self.cursor
		self.response()
		self.textview.scroll_to_iter(iterator, 0.001, use_align=align, xalign=1.0)
		self.response()
		return False

	def response(self):
		from gtk import events_pending, main_iteration
		while events_pending(): main_iteration(False)
#		self.__count += 1
#		print "Response count: ", self.__count
		return False

	def hide_completion_window(self):
		self.emit("hide-completion-window")
		return False

	def busy(self, busy=True):
		self.emit("private-busy", busy)
		return False

	def show_load_encoding_error_window(self, uri):
		self.emit("private-encoding-load-error", uri)
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

	def update_message(self, message, icon_name="scribes", time=5, priority="normal"):
		data = message, icon_name, time, priority
		self.emit("update-message", data)
		return False

	def hide_message(self):
		self.emit("hide-message")
		return False

	def set_message(self, message, icon_name="scribes"):
		data = message, icon_name
		self.emit("set-message", data)
		return False

	def unset_message(self, message, icon_name="scribes"):
		data = message, icon_name
		self.emit("unset-message", data)
		return False

	def get_toolbutton(self, name):
		toolbutton = None
		for toolbutton in self.toolbar.get_children():
			if name != toolbutton.get_property("name"): continue
			break
		return toolbutton

	def get_indentation(self, iterator=None):
		if iterator is None: iterator = self.cursor.copy()
		start = self.backward_to_line_begin(iterator.copy())
		if start.is_end() or start.ends_line(): return ""
		end = start.copy()
		while end.get_char() in (" ", "\t"): end.forward_char()
		return self.textbuffer.get_text(start, end)

	def get_line_indentation(self):
		indentation = []
		for character in self.get_line_text():
			if character not in (" ", "\t"): break
			indentation.append(character)
		return "".join(indentation)

	def get_newline_character(self):
		from Utils import NEWLINE_RE
		match = NEWLINE_RE.search(self.text)
		character = match.group(0) if match else "\n"
		return character

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

	def create_trigger(self, name, accelerator="", description="", category="", error=True, removable=True):
		from Trigger import Trigger
		trigger = Trigger(self, name, accelerator, description, category, error, removable)
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
		from string import whitespace
		text = self.textbuffer.get_text(start, end).strip(whitespace)
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
		from Utils import get_current_folder
		return get_current_folder(globals_)

	def uri_exists(self, uri):
		from Utils import uri_exists
		return uri_exists(uri)

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
		#FIXME: This function will soon be deprecated. It uses glade.
		# GTKBUILDER should be use instead.get_gui_object uses
		# GTKBUILDER.
		from os.path import join
		folder = self.get_current_folder(globals_)
		file_ = join(folder, basepath)
		from gtk.glade import XML
		glade = XML(file_, object_name, "scribes")
		return glade

	def get_gui_object(self, globals_, basepath):
		from Utils import get_gui_object
		return get_gui_object(globals_, basepath)

	def set_vm_interval(self):
		#FIXME: This function is deprecated!
		return

	def get_selection_range(self):
		if self.textbuffer.props.has_selection is False: return 0
		start, end = self.textbuffer.get_selection_bounds()
		return (end.get_line() - start.get_line()) + 1

	def get_file_monitor(self, path):
		from Utils import get_file_monitor
		return get_file_monitor(path)

	def get_folder_monitor(self, path):
		from Utils import get_folder_monitor
		return get_folder_monitor(path)

	def monitor_events(self, args, event_types):
		from Utils import monitor_events
		return monitor_events(args, event_types)

	def get_fileinfo(self, path):
		from Utils import get_fileinfo
		return get_fileinfo(path)

	def get_mimetype(self, path):
		from Utils import get_mimetype
		return get_mimetype(path)

	def begin_user_action(self):
		self.freeze()
		self.textbuffer.begin_user_action()
		return False

	def end_user_action(self):
		self.textbuffer.end_user_action()
		self.thaw()
		return False

	def execute(self, command):
		#FIXME: Not yet implemented!
		# Reserving this API.
		#command = None
		return False

	def is_delimeter(self, character):
		from Utils import is_delimeter
		return is_delimeter(character)

	def is_not_delimeter(self, character):
		from Utils import is_not_delimeter
		return is_not_delimeter(character)

	def enable_busy_pointer(self):
		print "Not yet implemented"
		return False

	def disable_busy_pointer(self):
		print "Not yet implemented"
		return False
