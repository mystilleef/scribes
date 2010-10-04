class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		from GUI.Manager import Manager
		Manager(manager, editor)
		editor.response()
#		from OpenButton import Button
#		Button(editor, manager)
#		from FileChooser import FileChooser
#		FileChooser(editor, manager)
#		from ComboBox import ComboBox
#		ComboBox(manager, editor)
#		from CancelButton import Button
#		Button(editor, manager)
#		from Window import Window
#		Window(editor, manager)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def show(self):
		self.__manager.emit("show-open-dialog-window")
		return
