name = "Automatic Word Completion Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.4
autoload = True
class_name = "WordCompletionPlugin"
short_description = "Automatic word completion for Scribes"
long_description = """Automatic word completion plugin for Scribes."""

class WordCompletionPlugin(object):

	def __init__(self, editor):
		self.__editor = editor

	def load(self):
		from WordCompletion.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		self.__manager.destroy()
		return
