from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from GenericActionHandler import Handler
		Handler(self, editor, self.__zeditor)
		from EditPointHandler import Handler
		Handler(self, editor, self.__zeditor)
		from WrapAbbreviationHandler import Handler
		Handler(self, editor, self.__zeditor)
		from SelectionMarker import Marker
		Marker(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		from zen_editor import ZenEditor
		self.__zeditor = ZenEditor(self, editor)
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.glade"))
		return

	gui = property(lambda self: self.__gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self, action):
		self.emit("mark-selection")
		self.emit("action", action)
		return False
