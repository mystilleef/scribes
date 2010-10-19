name = "Search and Replace Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "SearchSystemPlugin"
short_description = "Search and replace operations."
long_description = """This plug-in performs search and replace operations \
"""

class SearchSystemPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from SearchSystem.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
