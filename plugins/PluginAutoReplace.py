name = "Automatic Word Replacement"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "AutoReplacePlugin"
short_description = "Expand abbreviations in the buffer"
long_description = """\
The plug-in allows users to expand abbreviations in the editing area.
buffer. Via a graphic user interface, a user can map
the letter "u" to the word "you". Thus, anytime the user types "u"
followed by the "space" or "Enter" key, "u" is expanded to "you". This
plug-in implements the algorithm to perform such expansions.
"""

class AutoReplacePlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from AutoReplace.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
