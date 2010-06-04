from SCRIBES.SignalConnectionManager import SignalManager

class Activator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "fullview", self.__fullview_cb)
		self.connect(editor, "toolbar-is-visible", self.__visible_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__visible = False
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __show(self):
		if self.__visible: return False
		self.__editor.show_full_view()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __fullview_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __visible_cb(self, editor, visible):
		self.__visible = visible
		return False
