from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "update-message", self.__update_cb, True)
		self.connect(manager, "show-message", self.__show_cb, True)
		self.connect(manager, "fallback", self.__hide_cb)
		self.connect(editor, "message-bar-is-visible", self.__visible_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bar = editor.get_data("MessageBar")
		self.__visible = False
		self.__prev_message = ""
		self.__show_later = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __check_reshow(self):
		if self.__visible or self.__show_later is False: return False
		self.__show_later = False
		self.__show()
		return False

	def __show(self):
		self.__bar.show()
		return False

	def __hide(self):
		self.__bar.hide()
		return False

	def __reshow(self):
		self.__show_later = True
		self.__hide()
		return False

	def __update(self, message):
		if self.__visible and message == self.__prev_message: return False
		self.__prev_message = message
		self.__reshow() if self.__visible else self.__show()
#		self.__show()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		if self.__visible: return False
		self.__show()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __update_cb(self, manager, message, *args):
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(300, self.__update, message, priority=9999)
		return False

	def __visible_cb(self, editor, visible):
		self.__visible = visible
		self.__check_reshow()
		return False
