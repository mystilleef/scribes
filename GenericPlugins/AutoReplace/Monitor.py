from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class AutoReplaceMonitor(GObject):

	__gsignals__ = {
		"abbreviation-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, manager, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = self.__manager.connect("abbreviations-updated", self.__manager_abbreviations_updated_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__monitor_destroy_cb)
		self.__signal_id_3 = self.__editor.textview.connect("key-press-event", self.__monitor_key_press_event_cb)
		if self.__can_monitor is False:
			self.__editor.textview.handle_block(self.__signal_id_3)
		editor.response()

	def __init_attributes(self, manager, editor):
		# Reference to the AutoReplaceManager.
		self.__manager = manager
		# Reference to the editor.
		self.__editor = editor
		# A list of strings (abbreviations) to monitor.
		self.__abbreviation_list = []
		# Identifier for the "abbreviations-updated" signal.
		self.__signal_id_1 = None
		# Identifier for the "destroy" signal.
		self.__signal_id_2 = None
		# Identifier for the "key-press-event" signal.
		self.__signal_id_3 = None
		self.__can_monitor = True
		return

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __manager_abbreviations_updated_cb(self, manager, abbreviation_dictionary):
		self.__abbreviation_list = abbreviation_dictionary.keys()
		return

	def __monitor_destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor.textview)
		del self
		self = None
		return

	def __monitor_key_press_event_cb(self, textview, event):
		from gtk import keysyms
		if event.keyval in [keysyms.Return, keysyms.space]:
			if self.__found_abreviation(event.keyval): return True
		return False

	def __found_abreviation(self, keyval):
		self.__editor.block_response()
		word = self.__editor.word_to_cursor()
		self.__editor.unblock_response()
		if word is None: return False
		if word in self.__abbreviation_list:
			from gtk import keysyms
			if keyval == keysyms.space:
				self.emit("abbreviation-found", word + " ")
			else:
				self.emit("abbreviation-found", word + "\n")
			return True
		return False
