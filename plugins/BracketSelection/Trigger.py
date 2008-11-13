class BracketSelectionTrigger(object):
	"""
	This class implements triggers to select text within pair characters.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: An BracketSelectionTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_triggers()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__select_bracket_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = self.__signal_id_1 = None
		self.__match = editor.find_matching_bracket
		return

########################################################################
#
#							Public Method
#
########################################################################

	def destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.
		"""
		self.__destroy()
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __create_triggers(self):
		"""
		Create the trigger.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.
		"""
		self.__trigger = self.__editor.create_trigger("select_text_within_characters", "alt+b")
		self.__editor.add_trigger(self.__trigger)
		return

	def __select_text_within_pair_characters(self):
		"""
		Select text within pair characters if possible.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.

		@return: True if the operation succeeded.
		@rtype: A Boolean object.
		"""
		open_pair_characters = ("(", "[", "{", "<")
		cursor_iterator = self.__editor.get_cursor_iterator()
		transition_iterator = cursor_iterator.copy()
		while True:
			if transition_iterator.is_start(): break
			transition_iterator.backward_char()
			if not (transition_iterator.get_char() in open_pair_characters): continue
			transition_iterator.forward_char()
			iterator = self.__match(transition_iterator.copy())
			if not iterator: return False
			if iterator.get_offset() < cursor_iterator.get_offset(): return False
			self.__editor.textbuffer.select_range(transition_iterator, iterator)
			return True
		return False

	def __destroy(self): 
		"""
		Destroy instance of this class.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: An BracketSelectionTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		del self
		self = None
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __select_bracket_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.

		@param trigger: A trigger for the pair character selection function.
		@type trigger: A Trigger object.
		"""
		if self.__select_text_within_pair_characters():
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "succeed")
		else:
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "fail")
		return
