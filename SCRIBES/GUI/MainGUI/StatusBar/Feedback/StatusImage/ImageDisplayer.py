class Displayer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("set-image", self.__set_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__image = editor.get_data("StatusImage")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self, image):
		from gtk import ICON_SIZE_MENU as SIZE
		if image: self.__image.set_from_icon_name(image, SIZE)
		self.__image.show() if image else self.__image.hide()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __set_cb(self, manager, image):
		from gobject import idle_add
		idle_add(self.__set, image, priority=9999)
		return False
