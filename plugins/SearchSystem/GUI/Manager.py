class Manager(object):
	
	def __init__(self, manager, editor):
		from Bar import Bar
		Bar(manager, editor)
		from Entry import Entry
		Entry(manager, editor)