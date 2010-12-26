name = "FocusLastDocument Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "FocusLastDocumentPlugin"
short_description = "Switch to previous window"
long_description = "Switch to previous window"

class FocusLastDocumentPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__manager = None

	def load(self):
		from FocusLastDocument.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		self.__manager.destroy()
		return
