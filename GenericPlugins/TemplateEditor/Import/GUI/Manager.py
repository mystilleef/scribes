class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from ImportButton import Button
		Button(manager, editor)
		from FileChooser import FileChooser
		FileChooser(manager, editor)
		from CancelButton import Button
		Button(manager, editor)
