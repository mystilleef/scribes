class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_draw_spaces_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		self.__trigger = self.__create_trigger()
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		return

	def __create_trigger(self):
		# Trigger to toggle white space.
		self.__trigger = self.__editor.create_trigger("show_white_spaces", "<alt>period")
		self.__editor.add_trigger(self.__trigger)
		return self.__trigger

	def __toggle_draw_spaces_cb(self, *args):
		from DrawWhitespaceMetadata import get_value, set_value
		value = False if get_value() else True
		set_value(value)
		if value:
			icon = "yes"
			message = "Showing whitespace"
		else:
			icon = "no"
			message = "Hiding whitespace"
		self.__editor.update_message(message, icon, 7)
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return
