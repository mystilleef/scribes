class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger = self.__create_trigger()
		from MenuItem import MenuItem
		self.__menuitem = MenuItem(editor)
		return

	def __create_trigger(self):
		trigger = self.__editor.create_trigger("show_template_editor", "<alt>F12")
		self.__editor.add_trigger(trigger)
		return trigger

	def __activate_cb(self, *args):
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show()
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		if self.__manager: self.__manager.destroy()
		if self.__menuitem: self.__menuitem.destroy()
		del self
		self = None
		return
