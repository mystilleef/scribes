class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__button.connect("toggled", self.__toggled_cb)
		self.__sigid2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__manager.connect("database-update", self.__update_cb)
		self.__set_properties()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_widget("SpellCheckButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return False

	def __update(self):
		self.__button.handler_block(self.__sigid1)
		from SpellCheckMetadata import get_value
		self.__button.set_active(get_value())
		self.__button.handler_unblock(self.__sigid1)
		return 

	def __set(self):
		from SpellCheckMetadata import set_value
		set_value(self.__button.get_active())
		return 

	def __set_properties(self):
		self.__update()
		return

	def __toggled_cb(self, *args):
		self.__set()
		return True

	def __update_cb(self, *args):
		self.__update()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return
