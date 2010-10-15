name = "Theme Selector Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "ThemeSelectorPlugin"
short_description = "Shows a window to change themes."
long_description = """Shows a window to change themes."""

class ThemeSelectorPlugin(object):

	def __init__(self, editor):
		editor.refresh()
		self.__editor = editor
		self.__trigger = None
		editor.refresh()

	def load(self):
		self.__editor.refresh()
		from ThemeSelector.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.refresh()
		return

	def unload(self):
		self.__editor.refresh()
		self.__trigger.destroy()
		self.__editor.refresh()
		return
