class Manager(object):

	def __init__(self, manager, editor):
		from LineLabel import Label
		Label(manager, editor)
		from SpinButton import SpinButton
		SpinButton(manager, editor)
		from Displayer import Displayer
		Displayer(manager, editor)
