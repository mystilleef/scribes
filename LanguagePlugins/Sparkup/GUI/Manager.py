class Manager(object):

	def __init__(self, manager, editor):
		from Entry import Entry
		Entry(manager, editor)
		from Displayer import Displayer
		Displayer(manager, editor)
