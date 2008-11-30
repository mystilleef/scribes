class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__show_cb)

	def __init_attributes(self, editor):
		self.__manager = None
		self.__editor = editor
		self.__trigger = self.__create_trigger("show-document-statistics", "alt+question")
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		triggers = (self.__trigger,)
		self.__editor.remove_triggers(triggers)
		if self.__manager: self.__manager.destroy()
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return

	def __show_cb(self, *args):
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show()
		return False
