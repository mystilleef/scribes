class Manager(object):

	def __init__(self, editor, manager):
		from Window import Window
		Window(editor, manager)
		from AddButton import Button
		Button(editor, manager)
		from FileChooser import FileChooser
		FileChooser(editor, manager)
		from CancelButton import Button
		Button(editor, manager)
