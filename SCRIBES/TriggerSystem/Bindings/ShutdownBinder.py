from Binder import BaseBinder

class Binder(BaseBinder):

	def __init__(self, editor):
		editor.response()
		BaseBinder.__init__(self, editor, "<ctrl>q", "shutdown")
		self.__editor = editor
		editor.response()

	def activate(self):
		self.__editor.shutdown()
		return False
