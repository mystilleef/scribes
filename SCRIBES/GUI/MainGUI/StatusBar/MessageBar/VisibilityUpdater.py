from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "animation", self.__animate_cb)
		self.connect(manager, "slide", self.__slide_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__visible = False
		self.__slide = ""
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self, animation_type):
		visible = self.__is_visible(animation_type)
		if self.__visible == visible: return False
		self.__visible = visible
		self.__manager.emit("visible", visible)
		return False

	def __is_visible(self, animation_type):
		if self.__slide == "down" and animation_type == "end": return False
		return True

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __slide_cb(self, manager, slide):
		self.__slide = slide
		return False

	def __animate_cb(self, manager, animation_type):
#		from gobject import idle_add
#		idle_add(self.__update, animation_type, priority=9999)
		self.__update(animation_type)
		return False
