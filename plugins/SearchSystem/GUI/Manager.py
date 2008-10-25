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
		from MatchCaseButton import Button
		Button(manager, editor)
		from MatchWordButton import Button
		Button(manager, editor)
		from NormalButton import Button
		Button(manager, editor)
		from ForwardButton import Button
		Button(manager, editor)
		from BackwardButton import Button
		Button(manager, editor)
		from EntryActivator import Activator
		Activator(manager, editor)
		from ButtonSwitcher import Switcher
		Switcher(manager, editor)
		from PreviousButton import Button
		Button(manager, editor)
		from NextButton import Button
		Button(manager, editor)
		from StopButton import Button
		Button(manager, editor)
		from FindButton import Button
		Button(manager, editor)
