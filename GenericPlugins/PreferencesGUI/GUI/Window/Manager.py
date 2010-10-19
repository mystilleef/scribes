class Manager(object):

	def __init__(self, manager, editor):
		from Initializer import Initializer
		Initializer(manager, editor)
		from Destroyer import Destroyer
		Destroyer(manager, editor)
		from Displayer import Displayer
		Displayer(manager, editor)
