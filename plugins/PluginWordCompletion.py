name = "Automatic Word Completion Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.4
autoload = True
class_name = "WordCompletionPlugin"
short_description = "Automatic word completion for Scribes"
long_description = """Automatic word completion plugin for Scribes."""

class WordCompletionPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		editor.response()

	def load(self):
		self.__editor.response()
		from WordCompletion.Manager import Manager
		self.__manager = Manager(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__manager.destroy()
		self.__editor.response()
		return
