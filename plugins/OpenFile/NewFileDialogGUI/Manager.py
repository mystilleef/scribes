class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		from FeedbackLabel import Label
		Label(manager, editor)
		from InfoLabel import Label
		Label(manager, editor)
		from FileCreator import Creator
		Creator(manager, editor)
		from Validator import Validator
		Validator(manager, editor)
		from Button import Button
		Button(manager, editor)
		from TextEntry import Entry
		Entry(manager, editor)
		from Window import Window
		Window(editor, manager)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def show(self):
		self.__manager.emit("show-newfile-dialog-window")
		return
