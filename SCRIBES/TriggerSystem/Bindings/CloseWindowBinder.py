from Binder import BaseBinder

class Binder(BaseBinder):

	def __init__(self, editor):
		editor.response()
		BaseBinder.__init__(self, editor, "<ctrl>w", "scribes-close-window")
		self.__editor = editor
		editor.response()

	def __document_is_empty(self):
		from string import whitespace
		if self.__editor.text.strip(whitespace): return False
		return True

	def activate(self):
		save = False if self.__editor.generate_filename and self.__document_is_empty() else True
		self.__editor.close(save)
		return False
