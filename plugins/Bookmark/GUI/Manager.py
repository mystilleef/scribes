class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		from Window import Window
		Window(manager, editor)
		from TreeView import TreeView
		TreeView(manager, editor)
		from LineProcessor import Processor
		Processor(manager, editor)
		manager.emit("gui-created")

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return False

	def show(self):
		self.__manager.emit("gui-created")
		self.__manager.emit("show-window")
		return
