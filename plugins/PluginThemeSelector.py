name = "Theme Selector Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "ThemeSelectorPlugin"
short_description = "Shows the theme selector."
long_description = """Shows the theme selector."""

class ThemeSelectorPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from ThemeSelector.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
