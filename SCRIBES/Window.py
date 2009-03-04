from gettext import gettext as _

class Window(object):
	"""
	This class defines the behavior of the window for the text editor.
	"""

	def __init__(self, editor, uri):
		self.__init_attributes(editor, uri)
		self.__set_properties()
		self.__sigid7 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid8 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid9 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid10 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid11 = editor.connect("readonly", self.__readonly_cb)
		self.__sigid13 = editor.connect("renamed-file", self.__renamed_file_cb)
		self.__sigid14 = editor.connect("bar-is-active", self.__active_cb)
		self.__sigid15 = editor.connect("fullscreen", self.__fullscreen_cb)
#		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.gui.get_widget("Window")
		self.__uri = str(uri) if uri else None
		self.__title = self.__set_title()
		self.__is_minimized = False
		self.__is_maximized = False
		self.__bar_is_active = False
		return

	def __destroy(self):
		return False

	def __set_properties(self):
		if self.__uri: self.__update_window_title(_('Loading "%s" ...') % self.__title)
		return

	def __update_window_title(self, title):
		self.__window.set_property("title", title)
		self.__window.set_data("minimized", self.__is_minimized)
		self.__window.set_data("maximized", self.__is_maximized)
		return False

	def __set_title(self):
		from gnomevfs import URI
		return URI(self.__uri).short_name.encode("utf-8") if self.__uri else _("Unsaved Document")

	def __set_readonly(self, readonly):
		title = self.__set_title()
		update = self.__update_window_title
		update("%s [READONLY]" % title) if readonly else update(title)
		return False

	def __precompile_methods(self):
		methods = (self.__focus_in_event_cb,
			self.__focus_out_event_cb, self.__focus_out_after_event_cb,
			self.__modified_file_cb)
		self.__editor.optimize(methods)
		return False

########################################################################
#
#					Signal and Event Callback Handlers
#
########################################################################

	def __checking_file_cb(self, editor, uri):
		self.__uri = uri
		self.__title = self.__set_title()
		self.__update_window_title(_('Loading "%s" ...') % self.__title)
		return False

	def __loaded_file_cb(self, *args):
		self.__title = self.__set_title()
		readonly = self.__editor.readonly
		self.__set_readonly(readonly) if readonly else self.__update_window_title(self.__title)
		return False

	def __load_error_cb(self, *args):
		self.__uri = None
		self.__title = self.__set_title()
		self.__update_window_title(self.__title)
		return False

	def __modified_file_cb(self, editor, modified):
		title = str(self.__editor.uri_object.short_name) if self.__editor.uri else _("Unsaved Document")
		set_title = self.__window.set_title
		set_title("*%s" % title) if modified else set_title(title)
		return False

	def __readonly_cb(self, editor, readonly):
		self.__set_readonly(readonly)
		return False

	def __renamed_file_cb(self, editor, uri, *args):
		from gnomevfs import URI
		self.__window.set_title(URI(uri).short_name)
		return False

	def __active_cb(self, editor, active):
		self.__bar_is_active = active
		return False

	def __fullscreen_cb(self, manager, fullscreen):
		self.__editor.response()
		self.__window.fullscreen() if fullscreen else self.__window.unfullscreen()
		self.__editor.response()
		return True
