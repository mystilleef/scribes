class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__undo_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__redo_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("undo", "<ctrl>z")
		self.__trigger2 = self.__create_trigger("redo", "<ctrl><shift>z")
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __undo_cb(self, *args):
		self.__editor.undo()
		return False

	def __redo_cb(self, *args):
		self.__editor.redo()
		return

	def __destroy(self):
		self.__editor.remove_trigger(self.__trigger1)
		self.__editor.remove_trigger(self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return False
