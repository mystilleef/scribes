name = "Bracket Completion Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "BracketCompletionPlugin"
short_description = "Bracket completion operations."
long_description = """This plug-in performs bracket completion operations"""

class BracketCompletionPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__manager = None

	def load(self):
		from BracketCompletion.Manager import BracketManager
		self.__manager = BracketManager(self.__editor)
		return

	def unload(self):
		self.__manager.destroy()
		return
