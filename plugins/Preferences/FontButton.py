class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__button.connect("font-set", self.__set_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("database-update", self.__update_cb)
		self.__set_properties()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_widget("FontButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return False

	def __set_properties(self):
		self.__update()
		return

	def __set(self):
		font_name = self.__button.get_font_name()
		from FontMetadata import set_value
		set_value(font_name)
		return False

	def __update(self):
		from FontMetadata import get_value
		font_name = get_value()
		self.__button.handler_block(self.__sigid1)
		self.__button.set_font_name(font_name)
		self.__button.handler_unblock(self.__sigid1)
		return False

	def __update_cb(self, *args):
		self.__update()
		return

	def __set_cb(self, *args):
		self.__set()
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return
