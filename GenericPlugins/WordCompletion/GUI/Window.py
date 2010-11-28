from SCRIBES.SignalConnectionManager import SignalManager

class Window(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "hide-completion-window", self.__hide_cb)
		self.connect(manager, "no-match-found", self.__hide_cb)
		self.connect(manager, "hide-window", self.__hide_cb)
		self.connect(manager, "show-window", self.__show_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

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
		if self.__visible: return True
		self.__window.show_all()
		self.__editor.emit("completion-window-is-visible", True)
		self.__visible = True
		return False

	def __hide(self):
		if self.__visible is False: return False
		self.__window.hide()
		self.__editor.emit("completion-window-is-visible", False)
		self.__visible = False
		return False

	def __precompile_methods(self):
		methods = (self.__hide, self.__show)
		self.__editor.optimize(methods)
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
