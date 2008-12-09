from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class MatchingBracketTrigger(GObject):
	"""
	This class implements an object that finds matching pair characters.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__find_matching_bracket_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)


	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __create_trigger(self):
		self.__trigger = self.__editor.create_trigger("find_matching_bracket", "alt+shift+b")
		self.__editor.add_trigger(self.__trigger)
		return

	def __find_matching_bracket_cb(self, trigger):
		result = self.__find_matching_bracket()
		if result:
			iterator = self.__editor.get_cursor_iterator()
			line = iterator.get_line() + 1
			from i18n import msg0001
			message = msg0001 % (line)
			self.__editor.feedback.update_status_message(message, "suceed")
		else:
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "fail")
		return

	def __find_matching_bracket(self):
		"""
		Find matching bracket, if any.

		@param self: Reference to the MatchingBracketTrigger instance.
		@type self: A MatchingBracketTrigger object.

		@return: True if a matching bracket was found.
		@rtype: A Boolean object.
		"""
		iterator = self.__editor.cursor
		match = self.__editor.find_matching_bracket(iterator.copy())
		if not match: return False
		self.__editor.textbuffer.place_cursor(match)
		self.__editor.move_view_to_cursor()
		return True

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AboutTrigger instance.
		@type self: An AboutTrigger object.

		@param trigger: Reference to the AboutTrigger instance.
		@type trigger: An AboutTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		del self
		self = None
		return
