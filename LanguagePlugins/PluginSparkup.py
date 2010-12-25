name = "Sparkup Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
languages = ["html", "xml", "css", "javascript", "php"]
autoload = True
class_name = "SparkupPlugin"
short_description = "Advanced dynamic templates for HTML/XML/Javascript/CSS"
long_description = "See http://net.tutsplus.com/articles/general/quick-tip-even-quicker-markup-with-sparkup/"

class SparkupPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from Sparkup.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
