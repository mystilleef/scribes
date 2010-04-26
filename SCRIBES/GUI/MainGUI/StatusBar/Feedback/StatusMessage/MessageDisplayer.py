from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "set-message", self.__set_cb)
		self.connect(editor, "message-bar-is-visible", self.__visible_cb, True)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = editor.get_data("StatusFeedback")
		self.__prev_message = ""
		self.__visible = False
		from collections import deque
		self.__queue = deque()
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __set(self, message):
		try:
			if self.__visible: raise ValueError
			self.__queue.clear()
			if self.__prev_message == message: return False
			self.__prev_message = message
			self.__label.set_label(message)
			self.__label.queue_resize()
			self.__editor.response()
		except ValueError:
			self.__queue.clear()
			self.__queue.append(message)
		return False

	def __check(self):
		if self.__visible or not self.__queue: return False
		self.__set(self.__queue[-1])
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __set_cb(self, manager, message):
		from gobject import idle_add
		idle_add(self.__set, message)
		return False

	def __visible_cb(self, editor, visible):
		self.__visible = visible
		from gobject import idle_add
		idle_add(self.__check)
		return False
