class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from PositionComboBox import ComboBox
		ComboBox(manager, editor)
		from SizeComboBox import ComboBox
		ComboBox(manager, editor)
		from FillColorButton import Button
		Button(manager, editor)
