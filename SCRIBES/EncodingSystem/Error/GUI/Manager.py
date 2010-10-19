class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from ComboBox import ComboBox
		ComboBox(manager, editor)
		from Label import Label
		Label(manager, editor)
		from OpenButton import Button
		Button(manager, editor)
		from CloseButton import Button
		Button(manager, editor)
