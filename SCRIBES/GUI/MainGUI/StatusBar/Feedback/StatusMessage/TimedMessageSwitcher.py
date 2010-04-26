from SCRIBES.SignalConnectionManager import SignalManager

class Switcher(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "update", self.__update_cb)
		self.connect(editor, "message-bar-is-visible", self.__visible_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__prev_message = ""
		self.__visible = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, message, image, time):
		try:
			self.__manager.emit("busy", True)
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			color = "red" if image in ("error", "gtk-dialog-error", "fail", "no",) else "dark green"
			if self.__visible and self.__prev_message == message:
				pass
			else:
				self.__manager.emit("update-message", message, True, False, color)
			self.__prev_message = message
			self.__timer = timeout_add(time * 1000, self.__reset, priority=9999)
		return False

	def __reset(self):
		self.__manager.emit("busy", False)
		self.__manager.emit("reset")
		return False 

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, message, image, time):
		from gobject import idle_add
		idle_add(self.__update, message, image, time, priority=9999)
		return False # This is a test message. I think it works well.

	def __visible_cb(self, editor, visible):
		self.__visible == visible
		return False
