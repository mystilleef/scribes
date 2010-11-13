from Signals import Signal 

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from LineJumper import Jumper
		Jumper(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.glade"))
		return

	gui = property(lambda self: self.__gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return

	def show(self):
		self.emit("show")
		return
