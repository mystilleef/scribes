from SCRIBES.SignalConnectionManager import SignalManager

class Button(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "show-window", self.__activate_cb)
		self.__sigid1 = self.connect(self.__button, "toggled", self.__toggled_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("WidgetTransparencyCheckButton")
		return

	def __update(self):
		from SCRIBES.WidgetTransparencyMetadata import set_value
		set_value(self.__button.get_active())
		return False

	def __reset(self):
		self.__button.handler_block(self.__sigid1)
		from SCRIBES.WidgetTransparencyMetadata import get_value
		self.__button.set_active(get_value())
		self.__button.handler_unblock(self.__sigid1)
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__reset)
		return False

	def __toggled_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__update, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
