class Manager(object):
	
	def __init__(self, manager, editor):
		from Bar import Bar
		Bar(manager, editor)
		from Entry import Entry
		Entry(manager, editor)
		from ComboBox import ComboBox
		ComboBox(manager, editor)
		from MenuButton import Button
		Button(manager, editor)
		from PopupMenu import PopupMenu
		PopupMenu(manager, editor)
