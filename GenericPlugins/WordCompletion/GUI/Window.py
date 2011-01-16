from SCRIBES.SignalConnectionManager import SignalManager

class Window(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "hide-completion-window", self.__hide_cb)
		self.connect(editor, "hide-completion-window", self.__hide_cb, True)
		self.connect(manager, "no-match-found", self.__hide_cb)
		self.connect(manager, "no-match-found", self.__hide_cb, True)
		self.connect(manager, "invalid-string", self.__hide_cb)
		self.connect(manager, "invalid-string", self.__hide_cb, True)
		self.connect(manager, "hide-window", self.__hide_cb)
		self.connect(manager, "hide-window", self.__hide_cb, True)
		self.connect(manager, "show-window", self.__show_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.gui.get_widget("Window")
		from gtk import keysyms
		self.__keys = [keysyms.Tab, keysyms.Right, keysyms.Left,
			keysyms.Home, keysyms.End, keysyms.Insert, keysyms.Delete,
			keysyms.Page_Up, keysyms.Page_Down, keysyms.Escape]
		self.__visible = False
		return

	def __destroy(self):
		self.disconnect()
		self.__window.destroy()
		del self
		return 

	def __show(self):
		if self.__visible: return False
		self.__visible = True
		self.__window.show_all()
		self.__editor.emit("completion-window-is-visible", True)
		return False

	def __hide(self):
		if self.__visible is False: return False
		self.__window.hide()
		self.__visible = False
		self.__editor.emit("completion-window-is-visible", False)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False
