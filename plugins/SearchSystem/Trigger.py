class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__show_cb)
		self.__editor.get_toolbutton("SearchToolButton").props.sensitive = True

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.__create_trigger("show_findbar", "ctrl - f")
		self.__manager = None
		return

	def __create_trigger(self, name, shortcut):
		# Trigger to show the goto bar.
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __show_cb(self, *args):
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return
