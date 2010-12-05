name = "LastSessionLoader Plugin"
authors = ["Your Name <youremailaddress@gmail.com>"]
version = 0.1
autoload = True
class_name = "LastSessionLoaderPlugin"
short_description = "A short description"
long_description = "A long description"

class LastSessionLoaderPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from LastSessionLoader.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return

