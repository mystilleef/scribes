class Button(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("toggled", self.__toggled_cb)
		self.__sigid3 = manager.connect("search-type-flag", self.__update_cb)
		self.__button.props.active = False
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.menu_gui.get_widget("BackwardButton")
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
		set_value("backward")
		return

	def __set_active(self, search_type):
		self.__button.handler_block(self.__sigid2)
		self.__button.props.active = True if search_type == "backward" else False
		self.__button.handler_unblock(self.__sigid2)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggled_cb(self, manager, *args):
		self.__manager.emit("reset")
		self.__update_database()
		return False

	def __update_cb(self, manager, search_type):
		self.__set_active(search_type)
		return False
