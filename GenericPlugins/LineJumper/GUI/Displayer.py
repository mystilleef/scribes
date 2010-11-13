from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "show", self.__show_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "destroy", self.__quit_cb)
		self.__sig1 = self.connect(self.__view, "focus-in-event", self.__hide_cb)
		self.__sig2 = self.connect(self.__view, "button-press-event", self.__hide_cb)
		self.__sig3 = self.connect(self.__window, "key-press-event", self.__key_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__window = editor.window
		self.__container = manager.gui.get_object("Alignment")
		self.__visible = False
		self.__blocked = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __show(self):
		if self.__visible: return False
		self.__unblock()
		self.__editor.add_bar_object(self.__container)
		self.__visible = True
		return False

	def __hide(self):
		if self.__visible is False: return False
		self.__block()
		self.__view.grab_focus()
		self.__editor.remove_bar_object(self.__container)
		self.__editor.hide_message()
		self.__visible = False
		return False

	def __block(self):
		if self.__blocked: return False
		self.__view.handler_block(self.__sig1)
		self.__view.handler_block(self.__sig2)
		self.__window.handler_block(self.__sig3)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__view.handler_unblock(self.__sig1)
		self.__view.handler_unblock(self.__sig2)
		self.__window.handler_unblock(self.__sig3)
		self.__blocked = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide)
		return False

	def __key_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__manager.emit("hide")
		return True
