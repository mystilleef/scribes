from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):
	"""
	This class implements timed feedback messages. These are messages that appear for a short period
	of time, usually between 3 and 10 seconds, and they disappear. It also checks the priority of
	the message. Lower priority messages are discarded if the current message is still showing. 
	If the new message and the old message are the same, then only the timer is updated, not the 
	message. This saves animation cycles.
	
	#FIXME: I think priority checks and similarity checks should be performed by another class.
			This class should focus mainly on timing.
	process.
	"""

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "update-message", self.__update_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		self.__previous_message = ""
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self, data):
		same_message = self.__is_same_message(data[0])
		if same_message is False: self.__reset()
		self.__busy = True
		self.__manager.emit("busy", True)
		self.__remove_timer()
		from gobject import timeout_add
		message, image_id, time, priority = data
		self.__timer = timeout_add(time * 1000, self.__reset)
		if same_message: return False
		_images = ("error", "gtk-dialog-error", "fail", "no",)
		color = "red" if image_id in _images else "dark green"
		message, image_id, color, bold, italic, show_bar = message, image_id, color, True, False, True
		self.__manager.emit("format-feedback-message", (message, image_id, color, bold, italic, show_bar))
		return False

	def __is_same_message(self, message):
		if self.__busy is False: return False
		if self.__previous_message == message: return True
		self.__previous_message = message
		return False

	def __reset(self):
		self.__busy = False
		self.__manager.emit("busy", False)
		self.__manager.emit("reset")
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __update_cb(self, manager, data):
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__update, data, priority=PRIORITY_LOW)
		self.__update(data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
