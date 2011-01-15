name = "JavaScript Comment Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
languages = ["js", "php", "c", "cpp", "chdr"]
class_name = "JavaScriptCommentPlugin"
short_description = "Toggle comments in JavaScript source code"
long_description = """ "//" is used for single line comments. "/* */" is
used for multiline comments. """

class JavaScriptCommentPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from JavaScriptComment.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
