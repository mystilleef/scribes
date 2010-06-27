class AutoReplaceExpander(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = self.__manager.connect("abbreviations-updated", self.__expander_abbreviations_updated_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__expander_destroy_cb)
		self.__signal_id_3 = self.__manager.connect("abbreviation-found", self.__expander_abbreviation_found_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		# Reference to the AutoReplaceManager.
		self.__manager = manager
		# Reference to the editor.
		self.__editor = editor
		# A dictionary of abbreviations.
		self.__abbreviation_dictionary = {}
		# Identifier for the "abbreviations-updated" signal.
		self.__signal_id_1 = None
		# Identifier for the "destroy" signal.
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __expander_abbreviations_updated_cb(self, manager, abbreviation_dictionary):
		self.__abbreviation_dictionary = abbreviation_dictionary
		return

	def __expander_destroy_cb(self, manager):
		self.__abbreviation_dictionary.clear()
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__manager)
		del self
		self = None
		return

	def __expander_abbreviation_found_cb(self, manager, abbreviation):
		try:
			expanded_word = self.__abbreviation_dictionary[abbreviation[:-1]]
		except KeyError:
			return
		delimeter_character = abbreviation[-1]
		iterator = self.__editor.get_cursor_iterator()
		tmp_iterator = iterator.copy()
		for value in range(len(abbreviation[:-1])):
			self.__editor.response()
			tmp_iterator.backward_char()
		self.__editor.textbuffer.delete(tmp_iterator, iterator)
		self.__editor.textbuffer.insert_at_cursor(expanded_word + delimeter_character)
		from i18n import msg0001
		message = msg0001  % (abbreviation[:-1], expanded_word)
		self.__editor.feedback.update_status_message(message, "succeed")
		return
