class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from ExportButton import Button
		Button(manager, editor)
		from FilenameValidator import Validator
		Validator(manager, editor)
		from FileChooser import FileChooser
		FileChooser(manager, editor)
		from CancelButton import Button
		Button(manager, editor)
