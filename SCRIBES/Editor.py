from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_BOOLEAN
from gobject import TYPE_STRING, TYPE_OBJECT, TYPE_PYOBJECT
from Globals import data_folder, metadata_folder, home_folder, desktop_folder
from Globals import session_bus
from gnomevfs import URI
from gtksourceview2 import language_manager_get_default
from EncodingGuessListMetadata import get_value as get_encoding_guess_list
from EncodedFilesMetadata import get_value as get_encoding
from EncodingMetadata import get_value as get_encoding_list
from Utils import get_language
from SupportedEncodings import get_supported_encodings

class Editor(GObject):

	__gsignals__ = {
		# Nobody should listen to this signal. For internal use only.
		"close": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		# QUIT signal to all core objects. This signal is emitted only after
		# a file has been properly saved. For internal use only. PlEASE NEVER
		# EMIT THIS SIGNAL. This is the signal to listen to for proper cleanup
		# before exit.
		"quit": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"cursor-moved": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"ready": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"readonly": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"busy": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"checking-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"loading-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"loaded-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"load-error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"show-error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_OBJECT, TYPE_BOOLEAN)),
		"show-info": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_OBJECT, TYPE_BOOLEAN)),
		"modified-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"new-encoding-list": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update-encoding-guess-list": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"renamed-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"saved-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"save-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"private-save-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"save-error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_STRING)),
		"send-data-to-processor": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING
		)),
		"private-encoding-load-error": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"dbus-saved-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"dbus-save-error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_STRING)),
		"window-focus-out": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"combobox-encoding-data?": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"combobox-encoding-data": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, manager, uri=None, encoding=None):
		GObject.__init__(self)
		self.__sigid1 = self.connect("modified-file", self.__modified_file_cb)
		self.__sigid2 = self.connect("checking-file", self.__checking_file_cb)
		self.__sigid3 = self.connect("load-error", self.__load_error_cb)
		self.__sigid4 = self.connect_after("loaded-file", self.__loaded_file_cb)
		self.__sigid5 = self.connect_after("readonly", self.__readonly_cb)
		self.__sigid6 = self.connect("saved-file", self.__saved_file_cb)
		self.__init_attributes(manager, uri)
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
		# Object responsible for showing encoding error window. The window
		# allows users to load files with the correct encoding.
		from EncodingErrorManager import Manager
		Manager(self)
		from EncodingComboBoxDataManager import Manager
		Manager(self)
		# Register with instance manager after a successful editor
		# initialization.
		self.__imanager.register_editor(self)
		self.load_file(uri, encoding) if uri else self.__init_plugins()

	def __init_attributes(self, manager, uri):
		self.__contains_document = True if uri else False
		# True if file is saved.
		self.__modified = False
		self.__processing = False
		# Reference to instance manager.
		self.__imanager = manager
		from collections import deque
		# Key objects register with this object so that the editor does not
		# terminate before proper object cleanup.
		self.__registered_objects = deque([])
		from os.path import join
		glade_file = join(self.data_folder, "Editor.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		self.__uri = uri
		self.__started_plugins = False
		# True if editor is in readonly mode.
		self.__readonly = False
		self.__busy = 0
		return False

	def __destroy(self):
		self.disconnect_signal(self.__sigid1, self)
		self.disconnect_signal(self.__sigid2, self)
		self.disconnect_signal(self.__sigid3, self)
		self.disconnect_signal(self.__sigid4, self)
		self.disconnect_signal(self.__sigid5, self)
		self.disconnect_signal(self.__sigid6, self)
		self.__imanager.unregister_editor(self)
		self.__glade.get_widget("Window").destroy()
		del self
		self = None
		from gc import collect
		from thread import start_new_thread
		start_new_thread(collect, ())
		return False

	def __init_plugins(self):
		# FIXME: NOT YET IMPLEMENTED
		if self.__started_plugins: return False
		self.emit("ready")
		self.__started_plugins = True
		return False

	def __get_style_scheme_manager(self):
		from gtksourceview2 import style_scheme_manager_get_default
		manager = style_scheme_manager_get_default()
		self.__update_manager_search_path(manager, self.home_folder)
		return manager

	def __get_style_path(self, base_path):
		from os.path import join, exists
		path_ = join(self.home_folder, base_path)
		return path_ if exists(path_) else None

	def __update_manager_search_path(self, manager, home_folder):
		gedit_path = self.__get_style_path(".gnome2/gedit/styles")
		scribes_path = self.__get_style_path(".gnome2/scribes/styles")
		search_paths = manager.get_search_path()
		if gedit_path and not (gedit_path in search_paths): manager.prepend_search_path(gedit_path)
		if scribes_path and not (scribes_path in search_paths): manager.prepend_search_path(scribes_path)
		manager.force_rescan()
		return

################################################################
#
#						Public APIs
#
################################################################

	gui = property(lambda self: self.__glade)
	window = property(lambda self: self.gui.get_widget("Window"))
	textview = property(lambda self: self.gui.get_widget("ScrolledWindow").get_child())
	textbuffer = property(lambda self: self.textview.get_property("buffer"))
	id_ = property(lambda self: id(self))
	uri = property(lambda self: self.__uri)
	uris = property(lambda self: self.__imanager.get_uris())
	# All editor instances
	objects = instances = property(lambda self: self.__imanager.get_editor_instances())
	uri_object = property(lambda self: URI(self.__uri) if self.__uri else None)
	name = property(lambda self: URI(self.__uri).short_name if self.__uri else None)
	language_object = property(lambda self: get_language(self.__uri))
	language = property(lambda self: self.language_object.get_id() if self.language_object else None)
	language_manager = property(lambda self: language_manager_get_default())
	language_ids = property(lambda self: self.language_manager.get_language_ids())
	language_objects = property(lambda self: [self.language_manager.get_language(language) for language in self.language_ids])
	style_scheme_manager = property(__get_style_scheme_manager)
	readonly = property(lambda self: self.__readonly)
	modified = property(lambda self: self.__modified)
	contains_document = property(lambda self: self.__contains_document)
	encoding = property(lambda self:get_encoding(self.uri) if get_encoding(self.uri) else "utf-8")
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
	session_bus = property(lambda self: session_bus)
	save_processor = property(lambda self: self.__imanager.get_save_processor())
	supported_encodings = property(lambda self: get_supported_encodings())

	def new(self):
		return self.__imanager.open_files()

	def shutdown(self):
		self.close()
		return self.__imanager.close_all_windows()

	def close(self, save_first=True):
		self.emit("close", save_first)
		return False

	def refresh(self):
		#FIXME: NOT YET IMPLEMENTED
		return False

	def save_file(self, uri, encoding="utf-8"):
		# FIXME: NOT YET IMPLEMENTED
		return

	def load_file(self, uri, encoding, readonly=False):
		self.__contains_document = True
		from FileLoader import FileLoader
		FileLoader(self, uri, encoding, readonly)
		return False

	def open_file(self, uri, encoding="utf8"):
		return self.__imanager.open_files([uri], encoding)

	def open_files(self, uris, encoding="utf8"):
		return self.__imanager.open_files(uris, encoding)

	def focus_file(self, save_first=True):
		return self.__imanager.focus_file(uri)

	def close_file(self, uri):
		return self.__imanager.close_files([uri])

	def close_files(self, uris):
		return self.__imanager.close_files(uris)

	def init_authentication_manager(self):
		return self.__imanager.init_authentication_manager()

	def register_object(self, instance):
		self.__registered_objects.append(instance)
		return False

	def unregister_object(self, instance):
		self.__registered_objects.remove(instance)
		if not self.__registered_objects: self.__destroy()
		return False

	def calculate_resolution_independence(self, window, width, height):
		from Utils import calculate_resolution_independence
		return calculate_resolution_independence(window, width, height)

	def disconnect_signal(self, sigid, instance):
		from Utils import disconnect_signal
		return disconnect_signal(sigid, instance)

	def move_view_to_cursor(self):
		iterator = self.cursor
		self.textview.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
		return False

	def toggle_readonly(self):
		self.emit("readonly", False) if self.__readonly else self.emit("readonly", True)
		return

	def response(self):
		if self.__processing: return False
		self.__processing = True
		from gtk import events_pending, main_iteration
		while events_pending(): main_iteration(False)
		self.__processing = False
		return False

	def busy(self, busy=True):
		self.__busy = self.__busy + 1 if busy else self.__busy - 1
		if self.__busy < 0: self.__busy = 0
		busy = True if self.__busy else False
		self.emit("busy", busy)
		return False

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
########################################################################
#
#								Signal Listener
#
########################################################################

	def __readonly_cb(self, editor, readonly):
		self.__readonly = readonly
		return False

	def __modified_file_cb(self, editor, modified):
		self.__modified = modified
		return False

	def __checking_file_cb(self, editor, uri):
		self.__contains_document = True
		self.__uri = uri
		return False

	def __loaded_file_cb(self, *args):
		self.__init_plugins()
		return False

	def __load_error_cb(self, *args):
		self.__uri = None
		self.__contains_document = False
		self.__init_plugins()
		return False

	def __saved_file_cb(self, editor, uri, encoding):
		self.__uri = uri
		return False
