from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from FileOpener import Opener
		Opener(self, editor)
		from MatchFilterer import Filterer
		Filterer(self, editor)
		from DataGenerator import Generator
		Generator(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.glade"))
		return False

	gui = property(lambda self: self.__gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
