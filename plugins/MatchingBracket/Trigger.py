class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.__create_trigger()
		self.__manager = None
		return

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		self.__editor.remove_trigger(self.__trigger)
		del self
		self = None
		return False

	def __create_trigger(self):
		trigger = self.__editor.create_trigger("find_matching_bracket", "alt+shift+b")
		self.__editor.add_trigger(trigger)
		return trigger

	def __activate_cb(self, *args):
		try:
			self.__manager.match()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.match()
		return False

	def destroy(self):
		self.__destroy()
		return
