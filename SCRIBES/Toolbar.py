class Toolbar(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__add_toolbuttons()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("fullscreen", self.__fullscreen_cb)
		self.__set_visibility()
		self.__toolbar.set_property("sensitive", True)
		editor.register_object(self)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		editor.response()


	def __init_attributes(self, editor):
		self.__editor = editor
		self.__toolbar = editor.gui.get_widget("Toolbar")
		# Path to the font database.
		from os.path import join
		folder = join(editor.metadata_folder, "Preferences")
		file_path = join(folder, "MinimalMode.gdb")
		from gnomevfs import get_uri_from_local_path as get_uri
		self.__uri = get_uri(file_path)
		return

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
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

	def __show(self):
		self.__editor.response()
		self.__toolbar.show()
		self.__editor.response()
		return 

	def __hide(self):
		self.__editor.response()
		self.__toolbar.hide()
		self.__editor.response()
		return 

	def __set_visibility(self):
		from MinimalModeMetadata import get_value as minimal_mode
		self.__hide() if minimal_mode() else self.__show()
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fullscreen_cb(self, editor, fullscreen):
		self.__hide() if fullscreen else self.__set_visibility()
		return False

	def __changed_cb(self, *args):
		self.__set_visibility()
		return False
