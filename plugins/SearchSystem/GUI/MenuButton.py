class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("button-press-event", self.__button_press_event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("MenuButton")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__button.destroy()
		del self
		self = None
		return 

	def __toggle(self, event):
		self.__button.props.active = True
		self.__manager.emit("popup-menu", (event.button, event.time))
		return  
	
	def __untoggle(self):
		self.__button.props.active = False
		self.__manager.emit("hide-menu")
		return  

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __button_press_event_cb(self, button, event, *args):
		self.__untoggle() if self.__button.props.active else self.__toggle(event)
		return True
