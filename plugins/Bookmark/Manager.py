from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		editor.response()
		Signal.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from LineJumper import Jumper
		Jumper(self, editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from Utils import create_bookmark_image
		create_bookmark_image(editor)
		from MarkAdder import Adder
		Adder(self, editor)
		from MarkRemover import Remover
		Remover(self, editor)
		from MarginDisplayer import Displayer
		Displayer(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)
		from MarkReseter import Reseter
		Reseter(self, editor)
		from MarkUpdater import Updater
		Updater(self, editor)
		from Marker import Marker
		Marker(self, editor)
		from DatabaseReader import Reader
		Reader(self, editor)
		editor.response()

	def __init_attributes(self, editor):
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.glade"))
		return

	gui = property(lambda self: self.__gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def toggle(self):
		self.emit("toggle")
		return False

	def remove(self):
		self.emit("remove-all")
		return False

	def show(self):
		self.emit("show")
		return False
