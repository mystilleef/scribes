from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "show-full-view", self.__show_cb)
		self.connect(editor, "hide-full-view", self.__hide_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "show", self.__show_cb)
		self.connect(manager, "visible", self.__visible_cb)
		self.connect(manager, "animation", self.__animate_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__visible = False
		self.__animation = ""
		self.__reshow = False
		self.__rehide = False
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __hide(self):
		if self.__visible is False: return False
		if self.__animation == "end" and self.__visible: self.__manager.emit("_hide")
		if self.__animation == "begin": self.__rehide = True
		return False

	def __show(self):
		try:
			if self.__visible: raise ValueError
			self.__manager.emit("_show")
		except ValueError:
			self.__reshow = True
			self.__hide()
		return False

	def __check_show(self, visible):
		if self.__reshow is False or visible: return False
		self.__reshow = False
		self.__manager.emit("_show")
		return False

	def __check_hide(self, animation_type):
		if self.__rehide is False or animation_type == "begin": return False
		self.__rehide = False
		if self.__visible: self.__manager.emit("_hide")
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide, priority=9999)
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show, priority=9999)
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		from gobject import idle_add
		idle_add(self.__check_show, visible, priority=9999)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __animate_cb(self, manager, animation):
		self.__animation = animation
		from gobject import idle_add
		idle_add(self.__check_hide, animation, priority=9999)
		return False
