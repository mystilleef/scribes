class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__button.connect("value-changed", self.__changed_cb)
		self.__sigid2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__manager.connect("database-update", self.__update_cb)
		self.__sigid4 = self.__manager.connect("margin-display", self.__display_cb)
		self.__set_properties()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_widget("MarginSpinButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return False

	def __set(self):
		from MarginPositionMetadata import set_value
		set_value(int(self.__button.get_value()))
		return False

	def __update(self):
		from MarginPositionMetadata import get_value
		self.__button.handler_block(self.__sigid1)
		self.__button.set_value(get_value())
		self.__button.handler_unblock(self.__sigid1)
		return False

	def __set_properties(self):
		self.__button.props.sensitive = False
		self.__button.handler_block(self.__sigid1)
		self.__button.set_max_length(3)
		self.__button.set_width_chars(3)
		self.__button.set_digits(0)
		self.__button.set_increments(1, 5)
		self.__button.set_range(1, 120)
		from gtk import UPDATE_ALWAYS
		self.__button.set_update_policy(UPDATE_ALWAYS)
		self.__button.set_numeric(True)
		self.__button.set_snap_to_ticks(True)
		self.__button.handler_unblock(self.__sigid1)
		self.__update()
		return

	def __changed_cb(self, *args):
		self.__set()
		return True

	def __update_cb(self, *args):
		self.__update()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __display_cb(self, manager, sensitive):
		self.__button.props.sensitive = sensitive
		return False
