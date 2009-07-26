from Binder import BaseBinder

class Binder(BaseBinder):

	def __init__(self, editor):
		editor.response()
		BaseBinder.__init__(self, editor, "F11", "fullscreen")
		self.__editor = editor
		editor.response()

	def activate(self):
		self.__editor.toggle_fullscreen()
		return False
