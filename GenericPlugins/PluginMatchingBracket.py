name = "Matching Bracket Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "MatchingBracketPlugin"
short_description = "Find matching brackets."
long_description = """This plug-in the plug-in finds matching brackets \
in the editing area. Press (alt - shift - b) to find matching brackets. \
"""

class MatchingBracketPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from MatchingBracket.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
