name = "Bracket Indentation Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "BracketIndentationPlugin"
short_description = "Automatically format and indent brackets"
long_description = "Automatically format an indent brackets when enter key is pressed"

class BracketIndentationPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__manager = None

	def load(self):
		from BracketIndentation.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		self.__manager.destroy()
		return
