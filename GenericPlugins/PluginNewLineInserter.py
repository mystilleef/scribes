name = "NewLineInserter Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = False
class_name = "NewLineInserterPlugin"
short_description = "Doesn't work well. Detects unix, windows and apple line endings"
long_description = "Disabled by default. Doesn't work well. Tries to detect and use platform dependent line endings."

class NewLineInserterPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__manager = None

	def load(self):
		from NewLineInserter.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		self.__manager.destroy()
		return
