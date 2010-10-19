class Image(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("show-error", self.__update_cb, True)
		self.__sigid3 = editor.connect("show-info", self.__update_cb, False)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__image = manager.gui.get_widget("Image")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, error):
		from gtk import ICON_SIZE_DIALOG as DIALOG, STOCK_DIALOG_ERROR as ERROR
		from gtk import STOCK_DIALOG_INFO as INFO
		set_image = lambda image: self.__image.set_from_stock(image, DIALOG)
		set_image(ERROR) if error else set_image(INFO)
		return False

	def __update_cb(self, editor, title, message, window, busy, error):
		from gobject import idle_add
		idle_add(self.__update, error, priority=9999)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
