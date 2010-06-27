name = "JavaScript Comment Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
languages = ["js"]
class_name = "JavaScriptCommentPlugin"
short_description = "Toggle comments in JavaScript source code"
long_description = """ "//" is used for single line comments. "/* */" is
used for multiline comments. """

class JavaScriptCommentPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from JavaScriptComment.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
