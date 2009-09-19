class Entry(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show", self.__show_cb)
		self.__sigid3 = manager.connect("hide", self.__hide_cb)
		self.__sigid4 = self.__entry.connect("changed", self.__changed_cb)
		self.__sigid5 = self.__entry.connect("activate", self.__activate_cb)
		self.__sigid6 = manager.connect("focus-entry", self.__focus_cb)
		self.__entry.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_object("TextEntry")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__entry)
		self.__editor.disconnect_signal(self.__sigid5, self.__entry)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return False

	def __send(self):
		self.__manager.emit("pattern", self.__entry.get_text().strip())
		return False

	def __timeout_send(self):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(500, self.__send, priority=9999)
		return False

	def __clear(self):
		self.__entry.set_text("")
		self.__entry.grab_focus()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__clear)
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__clear)
		return False

	def __activate_cb(self, *args):
		self.__manager.emit("row-activated")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__manager.emit("entry-changed")
		from gobject import idle_add
		idle_add(self.__timeout_send)
		return False

	def __focus_cb(self, *args):
		self.__entry.grab_focus()
		return False
