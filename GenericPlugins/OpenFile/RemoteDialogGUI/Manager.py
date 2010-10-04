class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		from OpenButton import Button
		Button(editor, manager)
		from ComboBoxEntry import ComboBoxEntry
		ComboBoxEntry(editor, manager)
		from ComboBox import ComboBox
		ComboBox(manager, editor)
		from CancelButton import Button
		Button(editor, manager)
		from Window import Window
		Window(editor, manager)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def show(self):
		self.__manager.emit("show-remote-dialog-window")
		return
