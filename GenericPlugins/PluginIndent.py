name = "Indentation Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "IndentPlugin"
short_description = "Indent or unindent lines in Scribes."
long_description = """This plug-in indents or unindents a line or \ 
selected lines in Scribes. Press ctrl+t or ctrl+shift+t \
to indent or unindent lines."""

class IndentPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from Indent.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
