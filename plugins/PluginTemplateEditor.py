name = "Template Editor Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "TemplateEditorPlugin"
short_description = "This plugin shows the template editor."
long_description = """\
This plugin shows the template editor. The template editor allows users
to add, edit, remove, import or export templates.
"""

class TemplateEditorPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from TemplateEditor.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
