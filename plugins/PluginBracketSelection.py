name = "Bracket Selection Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "BracketSelectionPlugin"
short_description = "Bracket selection operations."
long_description = """Selects characters within brackets and quotes. Is
capable of incremental selection."""

class BracketSelectionPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from BracketSelection.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
