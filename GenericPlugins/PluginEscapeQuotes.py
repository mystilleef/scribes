name = "Escape Quotes Generic Plugin"
authors = ["Ib Lundgren <ib.lundgren@gmail.com"]
version = 0.3
autoload = True
class_name = "EscapeQuotesPlugin"
short_description = "Escape Quotes or Un-Escape Quotes"
long_description = """Use Ctrl+Shift+E to escape quotes and Ctrl+Alt+E to unescape them"""

class EscapeQuotesPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from EscapeQuotes.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
