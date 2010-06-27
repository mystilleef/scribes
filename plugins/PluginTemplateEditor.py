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
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from TemplateEditor.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
