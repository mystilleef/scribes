from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class PreferencesTrigger(GObject):
	"""
	This class creates an object that shows the text editor's open
	dialog.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the PreferencesTrigger instance.
		@type self: An PreferencesTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_preferences_dialog_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the PreferencesTrigger instance.
		@type self: A PreferencesTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None
		self.__trigger = None
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the PreferencesTrigger instance.
		@type self: A PreferencesTrigger object.
		"""
		# Trigger to show the preferences dialog.
		self.__trigger = self.__editor.create_trigger("show_preference_dialog", "F12")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_preferences_dialog_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the PreferencesTrigger instance.
		@type self: A PreferencesTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.show_dialog()
		except AttributeError:
			from Manager import PreferencesManager
			self.__manager = PreferencesManager(self.__editor)
			self.__manager.show_dialog()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the destroy "signal" is emitted.

		@param self: Reference to the PreferencesTrigger instance.
		@type self: An PreferencesTrigger object.

		@param trigger: Reference to the PreferencesTrigger instance.
		@type trigger: An PreferencesTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		if self.__manager: self.__manager.emit("destroy")
		del self
		self = None
		return
