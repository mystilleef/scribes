class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger = self.__create_trigger()
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		return

	def __create_trigger(self):
		# Trigger to show a symbol browser.
		self.__trigger = self.__editor.create_trigger("show_python_symbol_browser", "F5")
		self.__editor.add_trigger(self.__trigger)
		return self.__trigger

	def __show_cb(self, *args):
		try:
			self.__manager.show_browser()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show_browser()
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return
