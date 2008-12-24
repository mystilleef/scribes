class Manager(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		from Window import Window
		Window(editor, manager)
		from AddButton import Button
		Button(editor, manager)
		from FileChooser import FileChooser
		FileChooser(editor, manager)
		from CancelButton import Button
		Button(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
