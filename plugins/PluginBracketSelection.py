name = "Bracket Selection Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "BracketSelectionPlugin"
short_description = "Bracket completion operations."
long_description = """This plug-in performs bracket completion operations"""

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
