name = "Automatic Word Completion Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.6
autoload = True
class_name = "WordCompletionPlugin"
short_description = "Automatic word completion for Scribes"
long_description = """Automatic word completion plugin for Scribes."""

class WordCompletionPlugin(object):

	def __init__(self, editor):
		self.__editor = editor

	def load(self):
		from WordCompletion.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
