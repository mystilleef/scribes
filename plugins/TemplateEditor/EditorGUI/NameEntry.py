class Entry(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__entry.connect("changed", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor 
		self.__entry = manager.editor_gui.get_widget("NameEntry")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__entry)
		del self
		self = None
		return False

	def __send_text_async(self):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(150, self.__send_async, priority=9999)
		return False
	
	def __send_async(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer1)
		except AttributeError:
			pass
		finally:
			self.__timer1 = idle_add(self.__send, priority=9999)
		return False

	def __send(self):
		self.__manager.emit("name-entry-string", self.__entry.get_text())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__send_text_async()
		return False
