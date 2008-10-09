from gettext import gettext as _

COLOR = "#06989A"
class Feedback(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__label.set_label("")
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid4 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid5 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid6 = editor.connect("save-error", self.__save_error_cb)
		self.__sigid7 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid8 = editor.connect("readonly", self.__readonly_cb)
		self.__sigid9 = editor.connect("update-message", self.__update_message_cb)
		self.__sigid10 = editor.connect("set-message", self.__set_message_cb)
		self.__sigid11 = editor.connect("unset-message", self.__unset_message_cb)
		editor.register_object(self)
		editor.response()
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__busy = False
		from collections import deque
		self.__queue = deque([])
		self.__label = editor.gui.get_widget("StatusFeedback")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor)
		self.__editor.disconnect_signal(self.__sigid11, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__saved_file_cb, self.__modified_file_cb,
			self.__update_message_cb, self.__set_message_cb,
			self.__unset_message_cb)
		self.__editor.optimize(methods)
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __set_label(self, message=None, bold=False, italic=False, color=None):
		try:
			if not message: raise ValueError
			if color: message = "<span foreground='%s'>" % color + message + "</span>"
			if bold: message =  "<b>" + message + "</b>"
			if italic: message = "<i>" + message + "</i>"
			self.__label.set_label(message)
		except ValueError:
			self.__label.set_label("")
		return False

	def __set_default_message(self):
		try:
			if self.__queue: raise ValueError
			if not self.__editor.uri: raise TypeError
			filename = self.__get_filename(self.__editor.uri)
			self.__set_label(filename + _(" [modified]"), italic=True) if self.__editor.modified else self.__set_label(filename, bold=True)
		except ValueError:
			self.__set_label(self.__queue[-1], True, False, COLOR)
		except TypeError:
			self.__set_label()
		finally:
			self.__busy = False
		return False

	def __update_message(self, message, time=5, color=COLOR):
		self.__busy = True
		self.__set_label(message, True, False, color)
		from gobject import timeout_add
		timeout_add(time*1000, self.__set_default_message, priority=9999)
		return False

	def __set_message(self, message, color=COLOR):
		self.__queue.append(message)
		self.__set_label(message, True, False, color)
		return False

	def __unset_message(self, message):
		try:
			self.__queue.remove(message)
		except ValueError:
			pass
		if self.__busy: return False
		from gobject import idle_add
		idle_add(self.__set_default_message, priority=9999)
		return False

	def __get_filename(self, uri):
		from gnomevfs import URI
		filename = str(URI(uri).path)
		filename = filename.replace(self.__editor.home_folder.rstrip("/"), "~")
		return filename

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_file_cb(self, editor, uri, *args):
		filename = self.__get_filename(uri)
		message = _("Loading %s") % filename
		from gobject import idle_add
		idle_add(self.__set_message, message, priority=9999)
		return False

	def __loaded_file_cb(self, editor, uri, *args):
		filename = self.__get_filename(uri)
		message = _("Loaded %s") % filename
		from gobject import idle_add
		self.__timer = idle_add(self.__update_message, message, priority=9999)
		message = _("Loading %s") % filename
		idle_add(self.__unset_message, message, priority=9999)
		return False

	def __saved_file_cb(self, *args):
		if self.__busy: return False
		filename = self.__get_filename(self.__editor.uri)
		message = _("Saved %s") % filename
		from gobject import idle_add
		self.__remove_timer()
		self.__timer = idle_add(self.__update_message, message, 3, priority=9999)
		return False

	def __modified_file_cb(self, *args):
		if self.__busy: return False
		from gobject import idle_add
		self.__timer = idle_add(self.__set_default_message, priority=9999)
		return False

	def __save_error_cb(self, editor, uri, *args):
		filename = self.__get_filename(uri)
		message = _("Failed to save '%s'") % filename
		from gobject import idle_add
		idle_add(self.__update_message, message, 7, "red", priority=9999)
		return False

	def __load_error_cb(self, editor, uri, *args):
		filename = self.__get_filename(uri)
		message = _("Failed to load '%s'") % filename
		from gobject import idle_add
		idle_add(self.__update_message, message, 7, "red", priority=9999)
		return False

	def __readonly_cb(self, *args):
		return False

	def __update_message_cb(self, editor, message, icon_name, time):
		color = COLOR	
		if icon_name in ("error", "gtk-dialog-error", "fail", "no",): color = "red"
		self.__remove_timer()
		from gobject import idle_add
		self.__timer = idle_add(self.__update_message, message, time, color, priority=9999)
		return False

	def __set_message_cb(self, editor, message, icon_name):
		from gobject import idle_add
		idle_add(self.__set_message, message, priority=9999)
		return False

	def __unset_message_cb(self, editor, message, icon_name):
		from gobject import idle_add
		idle_add(self.__unset_message, message, priority=9999)
		return False
