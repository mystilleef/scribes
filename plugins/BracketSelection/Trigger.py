class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__select_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger = self.__create_trigger()
		return

	def __destroy(self): 
		if self.__manager: self.__manager.destroy()
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return

	def __create_trigger(self):
		trigger = self.__editor.create_trigger("select_text_within_characters", "alt+b")
		self.__editor.add_trigger(trigger)
		return trigger

	def __select_cb(self, *args):
		try:
			self.__manager.select()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.select()
		return

	def destroy(self):
		self.__destroy()
		return
