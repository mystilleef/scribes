name = "Bracket Highlight Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "BracketHighlightPlugin"
short_description = "Highlight region between matching pair characters."
long_description = """Highlight region between matching pair characters.
"""

class BracketHighlightPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__highlighter = None

	def load(self):
		from BracketHighlight.Highlighter import Highlighter
		self.__highlighter = Highlighter(self.__editor)
		return

	def unload(self):
		self.__highlighter.destroy()
		return
