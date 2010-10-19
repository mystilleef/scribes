from Binder import BaseBinder

class Binder(BaseBinder):

	def __init__(self, editor):
		BaseBinder.__init__(self, editor, "<ctrl>w", "scribes-close-window")
		self.__editor = editor

	def activate(self):
		self.__editor.close()
		return False
