class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("toggled", self.__toggled_cb)
		self.__sigid3 = manager.connect("hide-menu", self.__hide_cb)
		self.__sigid4 = manager.connect("hide-bar", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("MenuButton")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return 

	def __toggle(self):
		self.__manager.emit("popup-menu")
		return

	def __untoggle(self):
		self.__manager.emit("hide-menu")
		return  

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggled_cb(self, *args):
		self.__untoggle() if not self.__button.props.active else self.__toggle()
		return True

	def __hide_cb(self, *args):
		if self.__button.props.active: self.__button.props.active = False
		return False
