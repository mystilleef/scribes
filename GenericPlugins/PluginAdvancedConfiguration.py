name = "Advanced configuration plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "AdvancedConfigurationPlugin"
short_description = "Shows the advanced configuration window."
long_description = """Shows the advanced configuration window. The
window allows user to configure advanced options provided by the
editor."""

class AdvancedConfigurationPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from AdvancedConfiguration.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
