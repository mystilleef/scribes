name = "Document Switcher"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "DocumentSwitcherPlugin"
short_description = "Use (ctrl - tab) to switch between documents."
long_description = """\
Use (ctrl - tab) to switch between Scribes documents.
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
