class Manager(object):

	def __init__(self, manager, editor):
		from ButtonSwitcher import Switcher
		Switcher(manager, editor)
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
#		from MatchCaseButton import Button
#		Button(manager, editor)
		from MatchWordButton import Button
		Button(manager, editor)
#		from MenuComboBox import ComboBox
#		ComboBox(manager, editor)
		from EntryActivator import Activator
		Activator(manager, editor)
		from PreviousButton import Button
		Button(manager, editor)
		from NextButton import Button
		Button(manager, editor)
		from StopButton import Button
		Button(manager, editor)
		from FindButton import Button
		Button(manager, editor)
		from ReplaceWidgetDisplayer import Displayer
		Displayer(manager, editor)
		from ReplaceEntry import Entry 
		Entry(manager, editor)
		from ReplaceButton import Button
		Button(manager, editor)
		from ReplaceAllButton import Button
		Button(manager, editor)
