class Feedback(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("pattern", self.__pattern_cb)
		self.__sigid3 = manager.connect("filtered-files", self.__files_cb)
		self.__sigid4 = manager.connect("entry-changed", self.__changed_cb)
		self.__sigid5 = manager.connect("current-path", self.__path_cb)
		self.__sigid6 = manager.connect("formatted-files", self.__formatted_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__path = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return False

	def __clear(self, pattern):
		if pattern: return False
		self.__manager.emit("clear-message")
		return False

	def __search(self):
		message = _("<span foreground='brown'><i>searching please wait...</i></span>")
		self.__manager.emit("message", message)
		return False

	def __message(self, files):
		try:
			from gobject import timeout_add
			if not files: raise ValueError
			message = _("<span foreground='blue'><b>%s matches found</b></span>") % len(files)
			self.__manager.emit("message", message)
			self.__timer = timeout_add(5000, self.__clear, "")
		except ValueError:
			message = _("<span foreground='red'><b>No match found</b></span>")
			self.__manager.emit("message", message)
			self.__timer = timeout_add(7000, self.__clear, "")
		return False

	def __current_path(self, uri):
		self.__path = uri
		message = _("<span foreground='brown'><i>updating search path please wait...</i></span>")
		self.__manager.emit("message", message)
		return False

	def __path_message(self):
		from gio import File
		path = File(self.__path).get_path()
		message = _("<span foreground='blue'><b>%s is the current search path</b></span>") % path
		self.__manager.emit("message", message)
		from gobject import timeout_add
		self.__timer = timeout_add(5000, self.__clear, "")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __pattern_cb(self, manager, pattern):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__clear, pattern, priority=9999)
		return False

	def __files_cb(self, manager, files):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__message, files, priority=9999)
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__search, priority=9999)
		return False

	def __path_cb(self, manager, uri):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__current_path, uri, priority=9999)
		return False

	def __formatted_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__path_message, priority=9999)
		return False
