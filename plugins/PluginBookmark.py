name = "Bookmark Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "BookmarkPlugin"
short_description = "Bookmark operations."
long_description = """This plug-in performs operations to bookmark \
lines."""

class BookmarkPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from Bookmark.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
