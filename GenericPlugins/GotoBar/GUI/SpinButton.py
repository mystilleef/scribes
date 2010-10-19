class SpinButton(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-bar", self.__show_cb)
		self.__sigid3 = self.__button.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__button.connect("value-changed", self.__changed_cb)
		self.__sigid5 = self.__button.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("SpinButton")
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
		self.__editor.disconnect_signal(self.__sigid4, self.__button)
		self.__editor.disconnect_signal(self.__sigid5, self.__button)
		self.__button.destroy()
		del self
		self = None
		return 

	def __set_value(self):
		self.__button.handler_block(self.__sigid4)
		self.__button.set_range(1, self.__editor.textbuffer.get_line_count())
		line = self.__editor.cursor.get_line() + 1
		self.__button.set_value(line)
		self.__button.handler_unblock(self.__sigid4)
		self.__button.props.sensitive = True
		self.__button.grab_focus()
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__set_value()
		return False

	def __activate_cb(self, *args):
		self.__manager.emit("hide-bar")
		self.__manager.emit("line-number", self.__button.get_value())
		return False

	def __changed_cb(self, *args):
		self.__manager.emit("line-number", self.__button.get_value())
		return False
	
	def __key_press_event_cb(self, button, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide-bar")
		return False
