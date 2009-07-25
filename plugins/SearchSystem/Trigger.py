class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__show_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__show_replace_cb)
		self.__editor.get_toolbutton("SearchToolButton").props.sensitive = True
		self.__editor.get_toolbutton("ReplaceToolButton").props.sensitive = True

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("show_findbar", "<ctrl>f")
		self.__trigger2 = self.__create_trigger("show_replacebar", "<ctrl>r")
		self.__manager = None
		return

	def __create_trigger(self, name, shortcut):
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

	def __show_replace_cb(self, *args):
		try:
			self.__manager.show_replacebar()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show_replacebar()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		triggers = (self.__trigger1, self.__trigger2)
		self.__editor.remove_triggers(triggers)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		del self
		self = None
		return
