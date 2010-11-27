name = "Document Switcher"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "DocumentSwitcherPlugin"
short_description = "Functions to switch between windows."
long_description = """
		(ctrl+PageUp) - focus next window 
		(ctrl+PageDown) - focus previous window
"""

class DocumentSwitcherPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from DocumentSwitcher.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
