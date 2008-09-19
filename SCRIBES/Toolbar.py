class Toolbar(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__add_toolbuttons()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__set_visibility()
		self.__toolbar.set_property("sensitive", True)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__toolbar = editor.gui.get_widget("Toolbar")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __add_toolbuttons(self):
		from NewToolButton import Button
		# Create the new file toolbutton.
		self.__toolbar.insert(Button(self.__editor), 0)
		from OpenToolButton import Button
		# Create the open file toolbutton.
		self.__toolbar.insert(Button(self.__editor), 1)
		from SaveToolButton import Button
		# Create the rename file toolbutton.
		self.__toolbar.insert(Button(self.__editor), 2)
		# Create a toolbar separator.
		from gtk import SeparatorToolItem
		separator = SeparatorToolItem()
		separator.set_draw(True)
		separator.show()
		self.__toolbar.insert(separator, 3)
		from PrintToolButton import Button
		# Create the print file toolbutton.
		self.__toolbar.insert(Button(self.__editor), 4)
		# Create a toolbar separator.
		separator = SeparatorToolItem()
		separator.set_draw(True)
		separator.show()
		self.__toolbar.insert(separator, 5)
		from UndoToolButton import Button
		# Create the undo toolbutton.
		self.__toolbar.insert(Button(self.__editor), 6)
		from RedoToolButton import Button
		# Create the redo toolbutton.
		self.__toolbar.insert(Button(self.__editor), 7)
		# Create a separator.
		separator = SeparatorToolItem()
		separator.set_draw(True)
		separator.show()
		self.__toolbar.insert(separator, 8)
		from GotoToolButton import Button
		# Create the goto toolbutton.
		self.__toolbar.insert(Button(self.__editor), 9)
		from SearchToolButton import Button
		# Create the search toolbutton.
		self.__toolbar.insert(Button(self.__editor), 10)
		from ReplaceToolButton import Button
		# Create the search and replace toolbutton.
		self.__toolbar.insert(Button(self.__editor), 11)
		# Create a separator.
		separator = SeparatorToolItem()
		separator.set_draw(True)
		separator.show()
		self.__toolbar.insert(separator, 12)
		from PreferenceToolButton import Button
		# Create the preference toolbutton.
		self.__toolbar.insert(Button(self.__editor), 13)
		from HelpToolButton import Button
		# Create the help toolbutton.
		self.__toolbar.insert(Button(self.__editor), 14)
		# Create a separator.
		separator = SeparatorToolItem()
		separator.set_expand(True)
		separator.set_draw(False)
		separator.show()
		self.__toolbar.insert(separator, 15)
		# Create the Spinner.
		from Spinner import Spinner
		self.__toolbar.insert(Spinner(self.__editor), 16)
		return

	def __set_visibility(self):
		self.__toolbar.show()
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False
