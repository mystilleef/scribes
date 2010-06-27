name = "Escape Quotes Generic Plugin"
authors = ["Ib Lundgren <ib.lundgren@gmail.com"]
version = 0.3
autoload = True
class_name = "EscapeQuotesPlugin"
short_description = "Escape Quotes or Un-Escape Quotes"
long_description = """Use Ctrl+Shift+E to escape quotes and Ctrl+Alt+E to unescape them"""

class EscapeQuotesPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from EscapeQuotes.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
