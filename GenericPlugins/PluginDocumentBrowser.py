name = "Document Browser"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "DocumentBrowserPlugin"
short_description = "Show the document browser."
long_description = """\
Show the document browser.
"""

class DocumentBrowserPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from DocumentBrowser.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
