from Binder import BaseBinder

class Binder(BaseBinder):

	def __init__(self, editor):
		BaseBinder.__init__(self, editor, "F11", "fullscreen")
		self.__editor = editor

	def activate(self):
		self.__editor.toggle_fullscreen()
		return False
