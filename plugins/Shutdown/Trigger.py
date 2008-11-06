class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__shutdown_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger1 = self.__create_trigger("shutdown", "ctrl+shift+q")
		return

	def __destroy(self):
		self.__editor.remove_triggers((self.__trigger1,))
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		del self
		self = None
		return False

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __shutdown_cb(self, *args):
		self.__editor.shutdown()
		return False

	def destroy(self):
		self.__destroy()
		return
