name = "Bracket Completion Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "BracketCompletionPlugin"
short_description = "Bracket completion operations."
long_description = """This plug-in performs bracket completion operations"""

class BracketCompletionPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__manager = None
		editor.response()

	def load(self):
		self.__editor.response()
		from BracketCompletion.Manager import BracketManager
		self.__manager = BracketManager(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__manager.destroy()
		self.__editor.response()
		return
