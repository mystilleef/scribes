class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__button.connect("toggled", self.__toggled_cb)
		self.__sigid2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__manager.connect("get-data", self.__update_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_widget("TemplateIndentationCheckButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		return False

	def __update(self, active):
		self.__button.handler_block(self.__sigid1)
		self.__button.set_active(active)
		self.__button.handler_unblock(self.__sigid1)
		return False

	def __set(self):
		self.__manager.emit("set-data", self.__button.get_active())
		return False

	def __toggled_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set, priority=9999)
		return True

	def __update_cb(self, manager, active):
		from gobject import idle_add
		idle_add(self.__update, active, priority=9999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return
