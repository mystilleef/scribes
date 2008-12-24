class Label(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("error-message", self.__error_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__label = manager.gui.get_widget("ErrorLabel")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __set_message(self, message):
		string = "<span weight='bold' foreground='red'>%s</span>" % message
		self.__label.set_label(string)
		self.__label.show()
		self.__clear_label_async()
		return False

	def __clear_label_async(self):
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(11000, self.__clear, priority=9999)
		return False

	def __clear(self):
		self.__label.hide()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, manager, message):
		self.__set_message(message)
		return False
