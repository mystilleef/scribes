from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):
	"""
	This class is responsible for updating the message bar label and icon. Updates are performed
	when the message bar is NOT visible. The "message-bar-is-updated" signal is emitted after a
	successful update.
	"""

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "message-bar-is-visible", self.__visible_cb)
		self.connect(manager, "update-message-bar", self.__update_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Message bar label and image
		self.__label = editor.get_data("StatusFeedback")
		self.__image = editor.get_data("StatusImage")
		# Whether or not the message bar is visible.
		self.__visible = False
		# Feedback message that needs to be set when the message bar is not visible
		self.__data = None
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __check(self):
		if self.__data is None: return False
		self.__update(self.__data)
		return False

	def __update(self, data):
		# Update the message bar only if the bar is not visible.
		self.__data = data if self.__visible else None
		if self.__data is None: self.__set(data)
		return False

	def __set(self, data):
		message, image_id, show_bar = data
		self.__editor.refresh(False)
		self.__label.set_label(message)
		self.__editor.refresh(False)
		from gtk import ICON_SIZE_MENU as SIZE
		self.__editor.refresh(False)
		if image_id: self.__image.set_from_icon_name(image_id, SIZE)
		self.__image.show() if image_id else self.__image.hide()
		self.__editor.refresh(False)
		self.__manager.emit("message-bar-is-updated", (message, image_id, show_bar))
		return False

	def __update_cb(self, manager, data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__update, data, priority=PRIORITY_LOW)
#		self.__update(data)
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__check, priority=PRIORITY_LOW)
#		self.__check()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
