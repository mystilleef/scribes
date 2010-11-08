from gettext import gettext as _

from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):
	"""
	This module handles feedback messages that are shown indefinitely until they are
	removed.
	"""

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "loaded-file", self.__loaded_cb)
		self.connect(editor, "renamed-file", self.__loaded_cb)
		self.connect(editor, "saved-file", self.__saved_cb)
		self.connect(manager, "busy", self.__busy_cb)
		self.connect(manager, "fallback", self.__fallback_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		self.__default_name = ""
		self.__modified_name = ""
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __fallback_on_idle(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__fallback, priority=PRIORITY_LOW)
		return False

	def __fallback(self):
		if self.__busy: return False
		if self.__editor.uri:
			message, color = self.__default_name, ""
			bold, italic = True, False
			image_id, show_bar = "new", False
			data = message, image_id, color, bold, italic, show_bar
		else:
			data = "", "", "", False, False, False
		self.__manager.emit("format-feedback-message", data)
		return False

	def __update_names(self, uri):
		from gio import File
		filename = File(uri).get_parse_name()
		filename = filename.replace(self.__editor.home_folder.rstrip("/"), "~")
		self.__modified_name = filename + _(" [modified]")
		self.__default_name = filename
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fallback_cb(self, *args):
		self.__remove_timer()
		from gobject import timeout_add, PRIORITY_LOW as LOW
		self.__timer = timeout_add(300, self.__fallback_on_idle, priority=LOW)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False

	def __loaded_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__update_names, uri)
		return False

	def __saved_cb(self, editor, uri, *args):
		if editor.generate_filename is False: return False
		from gobject import idle_add
		idle_add(self.__update_names, uri)
		return False
