from Binder import BaseBinder

class Binder(BaseBinder):

	def __init__(self, editor):
		BaseBinder.__init__(self, editor, "<ctrl><shift><alt>w", "scribes-close-window-nosave")
		self.__editor = editor

	def activate(self):
		self.__editor.close(False)
		return False
