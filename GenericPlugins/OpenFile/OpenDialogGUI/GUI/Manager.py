class Manager(object):

	def __init__(self, manager, editor):
		from Window.Manager import Manager
		Manager(manager, editor)
		from FileChooser.Manager import Manager
		Manager(manager, editor)
		from ComboBox import ComboBox
		ComboBox(manager, editor)
		from OpenButton import Button
		Button(manager, editor)
		from CancelButton import Button
		Button(manager, editor)
