class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		from Entry import Entry
		Entry(manager, editor)
		from Displayer import Displayer
		Displayer(manager, editor)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def show(self):
		self.__manager.emit("show")
		return False

	def destroy(self):
		del self
		return False
