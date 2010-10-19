name = "Bracket Selection Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.4
autoload = True
class_name = "BracketSelectionPlugin"
short_description = "Bracket selection operations."
long_description = """Selects characters within brackets and quotes. Is
capable of incremental selection."""

class BracketSelectionPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from BracketSelection.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
