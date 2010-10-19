name = "Bookmark Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.4
autoload = True
class_name = "BookmarkPlugin"
short_description = "Manage bookmarked lines in a file."
long_description = """Add or remove bookmarks to lines. Navigate to 
bookmarked lines via a browser. Press ctrl+b to add or remove 
bookmarks. Press ctrl+d to navigate to bookmarked lines."""

class BookmarkPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None
		
	def load(self):
		from Bookmark.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
