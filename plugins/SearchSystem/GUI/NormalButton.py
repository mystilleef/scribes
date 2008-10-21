class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("toggled", self.__toggled_cb)
		self.__sigid3 = manager.connect("database-update", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.menu_gui.get_widget("NormalButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __update_database(self):
		from ..SearchTypeMetadata import set_value
		set_value("normal")
		return

	def __set_active(self):
		self.__button.handler_block(self.__sigid2)
		from ..SearchTypeMetadata import get_value
		self.__button.props.active = True if get_value() == "normal" else False
		self.__button.handler_unblock(self.__sigid2)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggled_cb(self, manager, *args):
		self.__update_database()
		return False

	def __update_cb(self, *args):
		self.__set_active()
		return False
