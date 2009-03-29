class Initializer(object):

	def __init__(self, toolbar, editor):
		editor.response()
		# Create the new window toolbutton.
		from Toolbuttons.NewToolButton import Button
		toolbar.insert(Button(editor), 0)
		# Create the open file toolbutton.
		from Toolbuttons.OpenToolButton import Button
		toolbar.insert(Button(editor), 1)
		# Create the save toolbutton.
		from Toolbuttons.SaveToolButton import Button
		toolbar.insert(Button(editor), 2)
		# Toolbar separator.
		from Utils import new_separator
		toolbar.insert(new_separator(), 3)
		# Create the print toolbutton.
		from Toolbuttons.PrintToolButton import Button
		toolbar.insert(Button(editor), 4)
		# Toolbar separator
		toolbar.insert(new_separator(), 5)
		# Create the undo toolbutton.
		from Toolbuttons.UndoToolButton import Button
		toolbar.insert(Button(editor), 6)
		# Create the redo toolbutton.
		from Toolbuttons.RedoToolButton import Button
		toolbar.insert(Button(editor), 7)
		# Toolbar separator
		toolbar.insert(new_separator(), 8)
		# Create the jump to another line toolbutton.
		from Toolbuttons.GotoToolButton import Button
		toolbar.insert(Button(editor), 9)
		# Create the search toolbutton.
		from Toolbuttons.SearchToolButton import Button
		toolbar.insert(Button(editor), 10)
		# Create the replace toolbutton.
		from Toolbuttons.ReplaceToolButton import Button
		toolbar.insert(Button(editor), 11)
		# Toolbar separator
		toolbar.insert(new_separator(), 12)
		# Create the preference toolbutton.
		from Toolbuttons.PreferenceToolButton import Button
		toolbar.insert(Button(editor), 13)
		# Create the help toolbutton.
		from Toolbuttons.HelpToolButton import Button
		toolbar.insert(Button(editor), 14)
		# Toolbar separator.
		toolbar.insert(new_separator(False, True), 15)
		# Create the spinner.
		from Toolbuttons.Spinner import Spinner
		toolbar.insert(Spinner(editor), 16)
		editor.response()
