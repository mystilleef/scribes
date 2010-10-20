from SCRIBES.SignalConnectionManager import SignalManager

class Entry(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "hide-window", self.__focus_cb)
		self.connect(manager, "show-window", self.__focus_cb)
		self.connect(manager, "focus-entry", self.__focus_cb)
		self.connect(self.__entry, "changed", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_object("Entry")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self):
		pattern = self.__entry.get_text().strip()
		self.__manager.emit("search-pattern", pattern)
		return False

	def __update_timeout(self):
		from gobject import idle_add
		self.__timer = idle_add(self.__update, priority=99999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(350, self.__update_timeout, priority=99999)
		return False

	def __focus_cb(self, *args):
		self.__entry.grab_focus()
		return False
