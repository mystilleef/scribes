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
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from SelectionSearcher.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
