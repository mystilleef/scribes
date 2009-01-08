class Window(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("no-match-found", self.__hide_cb)
		self.__sigid3 = manager.connect("hide-window", self.__hide_cb)
		self.__sigid4 = manager.connect("show-window", self.__show_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=5555)

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
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__window.destroy()
		del self
		self = None
		return 

	def __show(self):
		if self.__visible: return True
		self.__window.show_all()
		self.__visible = True
		return False

	def __hide(self):
		if self.__visible is False: return False
		self.__window.hide()
		self.__visible = False
		return False #

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

