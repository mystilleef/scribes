from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "set-image", self.__set_cb)
		self.connect(editor, "message-bar-is-visible", self.__visible_cb, True)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__image = editor.get_data("StatusImage")
		self.__prev_image = ""
		self.__visible = False
		from collections import deque
		self.__queue = deque()
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __check(self):
		if self.__visible or not self.__queue: return False
		self.__set(self.__queue[-1])
		return False

	def __set(self, image):
		try:
			if self.__visible: raise ValueError
			self.__queue.clear()
			if self.__prev_image == image: return False
			self.__prev_image = image
			from gtk import ICON_SIZE_MENU as SIZE
			if image: self.__image.set_from_icon_name(image, SIZE)
			self.__image.show() if image else self.__image.hide()
			self.__editor.response()
		except ValueError:
			self.__queue.clear()
			self.__queue.append(image)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __set_cb(self, manager, image):
		from gobject import idle_add
		idle_add(self.__set, image)
		return False

	def __visible_cb(self, editor, visible):
		self.__visible = visible
		from gobject import idle_add
		idle_add(self.__check)
		return False
