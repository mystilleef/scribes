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
		editor.response()
		self.__editor = editor
		self.__highlighter = None
		editor.response()

	def load(self):
		self.__editor.response()
		from BracketHighlight.Highlighter import Highlighter
		self.__highlighter = Highlighter(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__highlighter.destroy()
		self.__editor.response()
		return
