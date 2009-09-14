class Feedback(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("pattern", self.__pattern_cb)
		self.__sigid3 = manager.connect("filtered-files", self.__files_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __pattern_message(self, pattern):
		try:
			if not pattern: raise ValueError
			message = _("<span foreground='brown'><i>searching please wait...</i></span>")
			self.__manager.emit("message", message)
		except ValueError:
			self.__manager.emit("clear-message")
		return False

	def __match_message(self, files):
		try:
			from gobject import timeout_add
			if not files: raise ValueError
			message = _("<span foreground='blue'><b>%s matches found</b></span>") % len(files)
			self.__manager.emit("message", message)
			self.__timer = timeout_add(5000, self.__pattern_message, "")
		except ValueError:
			message = _("<span foreground='red'><b>No match found</b></span>")
			self.__manager.emit("message", message)
			self.__timer = timeout_add(7000, self.__pattern_message, "")
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
			self.__timer = idle_add(self.__pattern_message, pattern, priority=9999)
		return False

	def __files_cb(self, manager, files):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__match_message, files, priority=9999)
		return False
