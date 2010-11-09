from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "show-full-view", self.__show_cb)
		self.connect(editor, "hide-full-view", self.__hide_cb)
#		self.connect(editor, "toolbar-is-visible", self.__toolbar_cb)
		self.connect(manager, "hide", self.__hide_cb, True)
		self.connect(manager, "show", self.__show_cb, True)
#		self.connect(manager, "visible", self.__visible_cb)
#		self.connect(manager, "animation", self.__animate_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__visible = False
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __hide(self):
		if self.__visible is False: return False
		self.__manager.emit("_hide")
		self.__visible = False
		return False

	def __show(self):
		if self.__visible: return False
		self.__manager.emit("_show")
		self.__visible = True
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
