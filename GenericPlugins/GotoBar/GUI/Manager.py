class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		from Bar import Bar
		Bar(manager, editor)
		from Label import Label
		Label(manager, editor)
		from SpinButton import SpinButton
		SpinButton(manager, editor)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return
