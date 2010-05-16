name = "Selection Search Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "SelectionSearcherPlugin"
short_description = "Search editing area for selected text."
long_description = """Highlights all regions where selected text is 
found in the editing area. Use <ctrl>g and <ctrl><shift>g for 
navigating found matches."""

class SelectionSearcherPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from SelectionSearcher.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
