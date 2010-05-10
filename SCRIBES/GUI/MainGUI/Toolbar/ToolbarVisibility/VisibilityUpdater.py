from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "animation", self.__animation_cb)
		self.connect(manager, "slide", self.__slide_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__slide = ""
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self, animation):
		if animation != "end": return False
		visible = False if self.__slide == "up" else True
		self.__manager.emit("visible", visible)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __animation_cb(self, manager, animation):
		self.__update(animation)
		return False

	def __slide_cb(self, manager, slide):
		self.__slide = slide
		return False
