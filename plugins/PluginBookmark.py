name = "Bookmark Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "BookmarkPlugin"
short_description = "Bookmark operations."
long_description = """This plug-in performs operations to bookmark \
lines."""

class BookmarkPlugin(object):
	"""
	This class initializes a plug-in that performs selection operations.
	"""

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
