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
		self.connect(editor, "set-message", self.__set_cb)
		self.connect(editor, "unset-message", self.__unset_cb)
		self.connect(manager, "reset", self.__reset_cb)
		self.connect(manager, "busy", self.__busy_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__queue = deque()
		self.__busy = False
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __set(self, data):
		self.__queue.append(data)
		from gobject import idle_add
		idle_add(self.__reset)
		return False

	def __unset(self, data):
		if data in self.__queue: self.__queue.remove(data)
		from gobject import idle_add
		idle_add(self.__reset, True)
		return False

	def __reset(self, ignore_busy=False):
		if ignore_busy is False and self.__busy: return False
		from gobject import idle_add
		if self.__queue:
			message, image_id = self.__queue[-1]
			bold, italic, color, show_bar = True, False, "brown", True
			data = message, image_id, color, bold, italic, show_bar
			idle_add(self.__manager.emit, "format-feedback-message", data)
		else:
			idle_add(self.__manager.emit, "fallback")
		return False

	def __set_cb(self, editor, data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__set, data, priority=PRIORITY_LOW)
		return False

	def __unset_cb(self, editor, data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__unset, data, priority=PRIORITY_LOW)
		return False

	def __reset_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__reset, priority=PRIORITY_LOW)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
